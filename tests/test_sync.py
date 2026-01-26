"""
Integration tests for jolly_flow sync functionality.

Tests cover:
- Full sync workflow
- Exclusion patterns
- Dry-run mode
- Configuration validation
- Error handling
"""

import pytest
import os
import tempfile
import shutil
import yaml
from pathlib import Path
from jolly_flow.sync.sync import sync_files, is_excluded


class TestIsExcluded:
    """Tests for exclusion pattern matching."""

    def test_exact_match(self):
        """Test exact filename match."""
        assert is_excluded("secret.md", ["secret.md"]) == True
        assert is_excluded("public.md", ["secret.md"]) == False

    def test_wildcard_extension(self):
        """Test wildcard pattern for extensions."""
        assert is_excluded("file.secret.md", ["*.secret.md"]) == True
        assert is_excluded("file.public.md", ["*.secret.md"]) == False

    def test_glob_pattern(self):
        """Test glob pattern matching."""
        assert is_excluded("private/secret.md", ["private/*"]) == True
        assert is_excluded("public/doc.md", ["private/*"]) == False

    def test_multiple_patterns(self):
        """Test matching against multiple patterns."""
        patterns = ["*.secret.md", ".env", "private/*"]
        assert is_excluded("file.secret.md", patterns) == True
        assert is_excluded(".env", patterns) == True
        assert is_excluded("private/data.md", patterns) == True
        assert is_excluded("public.md", patterns) == False

    def test_no_patterns(self):
        """Test with empty pattern list."""
        assert is_excluded("anyfile.md", []) == False


class TestSyncFiles:
    """Integration tests for the sync_files function."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary vault and repo directories."""
        vault_dir = tempfile.mkdtemp(prefix="test_vault_")
        repo_dir = tempfile.mkdtemp(prefix="test_repo_")
        yield vault_dir, repo_dir
        # Cleanup
        shutil.rmtree(vault_dir, ignore_errors=True)
        shutil.rmtree(repo_dir, ignore_errors=True)

    @pytest.fixture
    def basic_config(self, temp_dirs):
        """Create a basic sync configuration."""
        vault_dir, repo_dir = temp_dirs
        config_file = os.path.join(vault_dir, ".jolly-sync.yaml")

        config = {
            "vault_root": vault_dir,
            "repo_root": repo_dir,
            "sync": [
                {"source": "test.md", "dest": "README.md"}
            ]
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        return config_file, vault_dir, repo_dir

    def test_basic_sync(self, basic_config):
        """Test basic file synchronization."""
        config_file, vault_dir, repo_dir = basic_config

        # Create source file
        source_content = """---
title: Test
---
# Test Document

See [[Overview]] for details.
"""
        with open(os.path.join(vault_dir, "test.md"), "w") as f:
            f.write(source_content)

        # Run sync
        sync_files(config_file, dry_run=False)

        # Verify destination file exists
        dest_file = os.path.join(repo_dir, "README.md")
        assert os.path.exists(dest_file)

        # Verify transformations applied
        with open(dest_file, "r") as f:
            result = f.read()

        assert "---" not in result  # Frontmatter removed
        assert "title:" not in result
        assert "[[" not in result  # Wikilinks resolved
        assert "Overview" in result
        assert "# Test Document" in result  # Content preserved

    def test_exclusion_patterns(self, temp_dirs):
        """Test that excluded files are not synced."""
        vault_dir, repo_dir = temp_dirs
        config_file = os.path.join(vault_dir, ".jolly-sync.yaml")

        config = {
            "vault_root": vault_dir,
            "repo_root": repo_dir,
            "exclude": ["*.secret.md", "private/*"],
            "sync": [
                {"source": "public.md", "dest": "public.md"},
                {"source": "data.secret.md", "dest": "data.md"},
                {"source": "private/secret.md", "dest": "secret.md"}
            ]
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        # Create test files
        with open(os.path.join(vault_dir, "public.md"), "w") as f:
            f.write("Public content")
        with open(os.path.join(vault_dir, "data.secret.md"), "w") as f:
            f.write("Secret data")
        os.makedirs(os.path.join(vault_dir, "private"), exist_ok=True)
        with open(os.path.join(vault_dir, "private/secret.md"), "w") as f:
            f.write("Private secret")

        # Run sync
        sync_files(config_file, dry_run=False)

        # Verify only public file was synced
        assert os.path.exists(os.path.join(repo_dir, "public.md"))
        assert not os.path.exists(os.path.join(repo_dir, "data.md"))
        assert not os.path.exists(os.path.join(repo_dir, "secret.md"))

    def test_dry_run_mode(self, basic_config):
        """Test that dry-run mode doesn't write files."""
        config_file, vault_dir, repo_dir = basic_config

        # Create source file
        with open(os.path.join(vault_dir, "test.md"), "w") as f:
            f.write("Test content")

        # Run sync in dry-run mode
        sync_files(config_file, dry_run=True)

        # Verify no files were written
        dest_file = os.path.join(repo_dir, "README.md")
        assert not os.path.exists(dest_file)

    def test_missing_source_file(self, basic_config):
        """Test handling of missing source files."""
        config_file, vault_dir, repo_dir = basic_config

        # Don't create source file - it's missing
        # This should not crash, just warn
        sync_files(config_file, dry_run=False)

        # Should complete without error
        dest_file = os.path.join(repo_dir, "README.md")
        assert not os.path.exists(dest_file)

    def test_creates_dest_directories(self, temp_dirs):
        """Test that destination directories are created."""
        vault_dir, repo_dir = temp_dirs
        config_file = os.path.join(vault_dir, ".jolly-sync.yaml")

        config = {
            "vault_root": vault_dir,
            "repo_root": repo_dir,
            "sync": [
                {"source": "test.md", "dest": "docs/nested/README.md"}
            ]
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        # Create source file
        with open(os.path.join(vault_dir, "test.md"), "w") as f:
            f.write("Test content")

        # Run sync
        sync_files(config_file, dry_run=False)

        # Verify nested directories were created
        dest_file = os.path.join(repo_dir, "docs/nested/README.md")
        assert os.path.exists(dest_file)
        assert os.path.isfile(dest_file)

    def test_private_blocks_removed(self, basic_config):
        """Test that private blocks are removed during sync."""
        config_file, vault_dir, repo_dir = basic_config

        source_content = """Public content

<!-- private -->
This should not appear in the synced file.
Secret information here.
<!-- /private -->

More public content.
"""
        with open(os.path.join(vault_dir, "test.md"), "w") as f:
            f.write(source_content)

        # Run sync
        sync_files(config_file, dry_run=False)

        # Verify private content removed
        dest_file = os.path.join(repo_dir, "README.md")
        with open(dest_file, "r") as f:
            result = f.read()

        assert "Public content" in result
        assert "More public content" in result
        assert "Secret information" not in result
        assert "<!-- private -->" not in result

    def test_image_transformation(self, temp_dirs):
        """Test image syntax transformation."""
        vault_dir, repo_dir = temp_dirs
        config_file = os.path.join(vault_dir, ".jolly-sync.yaml")

        config = {
            "vault_root": vault_dir,
            "repo_root": repo_dir,
            "images": {
                "transform_paths": True,
                "dest_dir": "images"
            },
            "sync": [
                {"source": "test.md", "dest": "README.md"}
            ]
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        source_content = "Image: ![[screenshot.png]]\n\nAnother: ![[folder/diagram.jpg]]"
        with open(os.path.join(vault_dir, "test.md"), "w") as f:
            f.write(source_content)

        # Run sync
        sync_files(config_file, dry_run=False)

        # Verify image syntax transformed
        dest_file = os.path.join(repo_dir, "README.md")
        with open(dest_file, "r") as f:
            result = f.read()

        assert "![screenshot](./images/screenshot.png)" in result
        assert "![diagram](./images/diagram.jpg)" in result
        assert "![[" not in result  # No Obsidian syntax remaining

    def test_configuration_validation(self, temp_dirs):
        """Test that configuration validation catches errors."""
        vault_dir, repo_dir = temp_dirs
        config_file = os.path.join(vault_dir, ".jolly-sync.yaml")

        # Missing vault_root
        config = {
            "repo_root": repo_dir,
            "sync": []
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        with pytest.raises(ValueError, match="vault_root"):
            sync_files(config_file)

    def test_nonexistent_vault_root(self, temp_dirs):
        """Test handling of non-existent vault root."""
        vault_dir, repo_dir = temp_dirs
        config_file = os.path.join(vault_dir, ".jolly-sync.yaml")

        config = {
            "vault_root": "/nonexistent/path",
            "repo_root": repo_dir,
            "sync": []
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        with pytest.raises(ValueError, match="does not exist"):
            sync_files(config_file)

    def test_transformation_options(self, temp_dirs):
        """Test that transformation options can be disabled."""
        vault_dir, repo_dir = temp_dirs
        config_file = os.path.join(vault_dir, ".jolly-sync.yaml")

        config = {
            "vault_root": vault_dir,
            "repo_root": repo_dir,
            "transform": {
                "remove_frontmatter": False,  # Disabled
                "resolve_wikilinks": True,
                "remove_private_blocks": True
            },
            "sync": [
                {"source": "test.md", "dest": "README.md"}
            ]
        }

        with open(config_file, "w") as f:
            yaml.dump(config, f)

        source_content = """---
title: Test
---
Content with [[Link]]
"""
        with open(os.path.join(vault_dir, "test.md"), "w") as f:
            f.write(source_content)

        # Run sync
        sync_files(config_file, dry_run=False)

        # Verify frontmatter NOT removed (disabled), but wikilinks resolved
        dest_file = os.path.join(repo_dir, "README.md")
        with open(dest_file, "r") as f:
            result = f.read()

        assert "---" in result  # Frontmatter preserved
        assert "title: Test" in result
        assert "[[" not in result  # Wikilinks still resolved
        assert "Link" in result
