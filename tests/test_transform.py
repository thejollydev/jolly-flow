"""
Unit tests for jolly_flow sync transformation functions.

Tests cover:
- Frontmatter removal
- Wikilink resolution
- Private blocks removal
- Image path transformation
"""

import pytest
from jolly_flow.sync.transform import (
    remove_frontmatter,
    resolve_wikilinks,
    remove_private_blocks,
    transform_image_paths
)


class TestRemoveFrontmatter:
    """Tests for YAML frontmatter removal."""

    def test_basic_frontmatter_removal(self):
        """Test removing basic YAML frontmatter."""
        content = "---\ntitle: Test\n---\nContent here"
        result = remove_frontmatter(content)
        assert result == "Content here"

    def test_no_frontmatter(self):
        """Test content without frontmatter remains unchanged."""
        content = "Just content\nNo frontmatter"
        result = remove_frontmatter(content)
        assert result == content

    def test_multiple_dashes(self):
        """Test that only frontmatter dashes are removed."""
        content = "---\ntitle: Test\n---\nContent\n---\nMore content"
        result = remove_frontmatter(content)
        assert result == "Content\n---\nMore content"

    def test_multiline_frontmatter(self):
        """Test removing multiline frontmatter."""
        content = """---
title: Test
created: 2026-01-25
tags:
  - test
  - markdown
---
Content starts here"""
        result = remove_frontmatter(content)
        assert result == "Content starts here"

    def test_unicode_content(self):
        """Test handling unicode in content."""
        content = "---\ntitle: Test\n---\nContent with émojis 🎉 and ñ"
        result = remove_frontmatter(content)
        assert result == "Content with émojis 🎉 and ñ"

    def test_empty_frontmatter(self):
        """Test handling empty frontmatter."""
        content = "---\n---\nContent"
        result = remove_frontmatter(content)
        assert result == "Content"


class TestResolveWikilinks:
    """Tests for Obsidian wikilink resolution."""

    def test_basic_wikilink(self):
        """Test converting basic wikilink to text."""
        content = "See [[Overview]] for details"
        result = resolve_wikilinks(content)
        assert result == "See Overview for details"

    def test_wikilink_with_alias(self):
        """Test converting wikilink with alias."""
        content = "See [[Overview|this page]] for details"
        result = resolve_wikilinks(content)
        assert result == "See this page for details"

    def test_multiple_wikilinks(self):
        """Test converting multiple wikilinks."""
        content = "See [[Page1]] and [[Page2|second page]]"
        result = resolve_wikilinks(content)
        assert result == "See Page1 and second page"

    def test_nested_brackets(self):
        """Test handling nested brackets."""
        content = "[[Link with [[nested]] brackets]]"
        # This is an edge case - behavior depends on regex
        result = resolve_wikilinks(content)
        # Should handle outermost brackets
        assert "[[" not in result or result.count("[[") < content.count("[[")

    def test_wikilink_with_path(self):
        """Test wikilink with folder path."""
        content = "See [[folder/page|the page]]"
        result = resolve_wikilinks(content)
        assert result == "See the page"

    def test_no_wikilinks(self):
        """Test content without wikilinks remains unchanged."""
        content = "Regular markdown with [standard](link.md)"
        result = resolve_wikilinks(content)
        assert result == content


class TestRemovePrivateBlocks:
    """Tests for private block removal."""

    def test_basic_private_block(self):
        """Test removing basic private block."""
        content = "Public\n<!-- private -->Secret<!-- /private -->\nPublic"
        result = remove_private_blocks(content)
        assert result == "Public\n\nPublic"
        assert "Secret" not in result

    def test_multiple_private_blocks(self):
        """Test removing multiple private blocks."""
        content = """Public
<!-- private -->Secret1<!-- /private -->
Middle
<!-- private -->Secret2<!-- /private -->
End"""
        result = remove_private_blocks(content)
        assert "Secret1" not in result
        assert "Secret2" not in result
        assert "Public" in result
        assert "Middle" in result
        assert "End" in result

    def test_multiline_private_block(self):
        """Test removing multiline private block."""
        content = """Public content
<!-- private -->
This is
a multiline
secret
<!-- /private -->
More public content"""
        result = remove_private_blocks(content)
        assert "secret" not in result
        assert "Public content" in result
        assert "More public content" in result

    def test_case_insensitive_tags(self):
        """Test private tags are case insensitive."""
        content = "Public\n<!-- PRIVATE -->Secret<!-- /PRIVATE -->\nPublic"
        result = remove_private_blocks(content)
        assert "Secret" not in result

    def test_whitespace_in_tags(self):
        """Test handling whitespace in tags."""
        content = "Public\n<!--  private  -->Secret<!--  /private  -->\nPublic"
        result = remove_private_blocks(content)
        assert "Secret" not in result

    def test_no_private_blocks(self):
        """Test content without private blocks remains unchanged."""
        content = "All public content\nNo secrets here"
        result = remove_private_blocks(content)
        assert result == content


class TestTransformImagePaths:
    """Tests for Obsidian image syntax transformation."""

    def test_basic_image(self):
        """Test transforming basic image syntax."""
        content = "Image: ![[screenshot.png]]"
        result = transform_image_paths(content)
        assert result == "Image: ![screenshot](./images/screenshot.png)"

    def test_image_with_path(self):
        """Test transforming image with folder path."""
        content = "Image: ![[folder/screenshot.png]]"
        result = transform_image_paths(content)
        assert result == "Image: ![screenshot](./images/screenshot.png)"

    def test_multiple_images(self):
        """Test transforming multiple images."""
        content = "First: ![[img1.png]] Second: ![[img2.jpg]]"
        result = transform_image_paths(content)
        assert "![img1](./images/img1.png)" in result
        assert "![img2](./images/img2.jpg)" in result

    def test_custom_dest_dir(self):
        """Test using custom destination directory."""
        content = "Image: ![[test.png]]"
        result = transform_image_paths(content, dest_images_dir="assets")
        assert result == "Image: ![test](./assets/test.png)"

    def test_no_images(self):
        """Test content without images remains unchanged."""
        content = "Regular text with no images"
        result = transform_image_paths(content)
        assert result == content

    def test_preserve_standard_markdown_images(self):
        """Test that standard markdown images are preserved."""
        content = "Standard: ![alt](./path/image.png) Obsidian: ![[image.png]]"
        result = transform_image_paths(content)
        # Standard markdown should be preserved
        assert "![alt](./path/image.png)" in result
        # Obsidian syntax should be transformed
        assert "![image](./images/image.png)" in result


class TestIntegration:
    """Integration tests combining multiple transformations."""

    def test_full_transformation_pipeline(self):
        """Test applying all transformations together."""
        content = """---
title: Test Document
---
# Document

See [[Overview|the overview]] for details.

![[screenshot.png]]

<!-- private -->
This is secret information.
<!-- /private -->

Public content continues here.

Another link: [[Page]]
"""
        # Apply all transformations in order
        result = remove_frontmatter(content)
        result = resolve_wikilinks(result)
        result = remove_private_blocks(result)
        result = transform_image_paths(result)

        # Verify all transformations applied
        assert "---" not in result  # No frontmatter
        assert "title:" not in result
        assert "[[" not in result  # No wikilinks
        assert "secret" not in result  # No private blocks
        assert "![screenshot](./images/screenshot.png)" in result  # Images transformed
        assert "the overview" in result  # Wikilink alias preserved
        assert "Page" in result  # Basic wikilink converted

    def test_transformations_preserve_content(self):
        """Test that transformations don't remove wanted content."""
        content = """---
meta: data
---
Regular content
[[Link]]
<!-- private -->secret<!-- /private -->
![[image.png]]
More content"""

        result = remove_frontmatter(content)
        result = resolve_wikilinks(result)
        result = remove_private_blocks(result)
        result = transform_image_paths(result)

        assert "Regular content" in result
        assert "More content" in result
        assert len(result.strip()) > 0  # Content not empty
