import os
import yaml
import shutil
from pathlib import Path
from fnmatch import fnmatch
from typing import List
from .transform import (
    remove_frontmatter,
    resolve_wikilinks,
    remove_private_blocks,
    transform_image_paths
)

def is_excluded(file_path: str, exclusion_patterns: List[str]) -> bool:
    """Check if a file matches any exclusion pattern."""
    for pattern in exclusion_patterns:
        if fnmatch(file_path, pattern):
            return True
    return False

def sync_files(config_path: str, dry_run: bool = False):
    """
    Synchronize files from Obsidian vault to project repository.

    Args:
        config_path: Path to .jolly-sync.yaml configuration file
        dry_run: If True, show what would be synced without writing files
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    vault_root = config.get("vault_root")
    repo_root = config.get("repo_root")
    sync_list = config.get("sync", [])
    exclusion_patterns = config.get("exclude", [])

    # Image handling configuration
    images_config = config.get("images", {})
    copy_images = images_config.get("copy", False)
    images_dest_dir = images_config.get("dest_dir", "images")
    transform_images = images_config.get("transform_paths", True)

    # Transformation options
    transform_config = config.get("transform", {})
    do_remove_frontmatter = transform_config.get("remove_frontmatter", True)
    do_resolve_wikilinks = transform_config.get("resolve_wikilinks", True)
    do_remove_private_blocks = transform_config.get("remove_private_blocks", True)

    # Validate configuration
    if not vault_root:
        raise ValueError("Configuration missing required field: vault_root")
    if not repo_root:
        raise ValueError("Configuration missing required field: repo_root")
    if not os.path.exists(vault_root):
        raise ValueError(f"Vault root does not exist: {vault_root}")

    print(f"📁 Vault: {vault_root}")
    print(f"📦 Repo: {repo_root}")
    if exclusion_patterns:
        print(f"🚫 Exclusions: {', '.join(exclusion_patterns)}")
    print()

    for item in sync_list:
        source_rel = item.get("source")
        dest_rel = item.get("dest")

        if not source_rel or not dest_rel:
            print(f"⚠️ Skipping invalid sync item: {item}")
            continue

        # Check exclusion patterns
        if is_excluded(source_rel, exclusion_patterns):
            print(f"🚫 Excluded: {source_rel}")
            continue

        source_path = os.path.join(vault_root, source_rel)
        dest_path = os.path.join(repo_root, dest_rel)

        if not os.path.exists(source_path):
            print(f"⚠️ Source not found: {source_path}")
            continue

        print(f"🔄 Syncing: {source_rel} -> {dest_rel}")

        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Apply transformations based on configuration
        if do_remove_frontmatter:
            content = remove_frontmatter(content)
        if do_resolve_wikilinks:
            content = resolve_wikilinks(content)
        if do_remove_private_blocks:
            content = remove_private_blocks(content)
        if transform_images:
            content = transform_image_paths(content, images_dest_dir)

        if not dry_run:
            # Create destination directory
            dest_dir = os.path.dirname(dest_path)
            if dest_dir:
                os.makedirs(dest_dir, exist_ok=True)

            # Write transformed content
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Written: {dest_path}")

            # Copy images if configured
            if copy_images and transform_images:
            print(f"  🔍 Dry run: would write to {dest_path}")
