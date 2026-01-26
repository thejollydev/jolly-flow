# jolly-sync - Obsidian to Repository Synchronization

**Part of The Jolly Method** - Phase 3 Implementation

---

## Overview

The `jolly-sync` module synchronizes documentation from private Obsidian vaults to public code repositories, applying transformations to remove Obsidian-specific syntax and private content.

### What It Does

- **Copies** files from vault to repository based on `.jolly-sync.yaml` configuration
- **Transforms** Obsidian syntax to standard Markdown
- **Removes** private content and metadata
- **Filters** files using exclusion patterns

---

## Usage

### Basic Usage

```bash
# From within a project directory with .jolly-sync.yaml
jolly-flow sync

# Specify custom config file
jolly-flow sync --config path/to/.jolly-sync.yaml

# Dry-run mode (preview without writing)
jolly-flow sync --dry-run
```

### As a Module

```python
from jolly_flow.sync.sync import sync_files

# Run sync
sync_files(".jolly-sync.yaml", dry_run=False)
```

---

## Configuration

### Basic Configuration

Create a `.jolly-sync.yaml` file in your project vault:

```yaml
vault_root: "/home/user/Obsidian/MyProject"
repo_root: "/home/user/Projects/my-project"

sync:
  - source: "PROJECT-OVERVIEW.md"
    dest: "README.md"
  - source: "ARCHITECTURE.md"
    dest: "docs/ARCHITECTURE.md"
```

### Complete Configuration Schema

```yaml
# Required: Path to Obsidian vault
vault_root: "/path/to/vault"

# Required: Path to code repository
repo_root: "/path/to/repo"

# Optional: Files/patterns to exclude from sync
exclude:
  - "*.secret.md"        # Wildcard patterns
  - ".env"               # Exact filenames
  - "private/**"         # Directory patterns
  - "journals/**"        # Exclude all journals

# Optional: Image handling configuration
images:
  copy: false            # Whether to copy image files (default: false)
  dest_dir: "images"     # Destination directory for images (default: "images")
  transform_paths: true  # Transform ![[]] syntax (default: true)

# Optional: Transformation options (all default to true)
transform:
  remove_frontmatter: true      # Strip YAML frontmatter
  resolve_wikilinks: true       # Convert [[links]] to plain text
  remove_private_blocks: true   # Remove <!-- private --> sections
  remove_comments: false        # Remove HTML comments (not implemented yet)

# Required: List of files to sync
sync:
  - source: "SOURCE.md"    # Relative to vault_root
    dest: "DEST.md"        # Relative to repo_root
  - source: "docs/GUIDE.md"
    dest: "docs/GUIDE.md"
```

---

## Transformations

### 1. Frontmatter Removal

**Before:**
```markdown
---
title: My Document
created: 2026-01-25
tags: [test, markdown]
---
# Content starts here
```

**After:**
```markdown
# Content starts here
```

---

### 2. Wikilink Resolution

**Before:**
```markdown
See [[Overview]] for details.
Check out [[Architecture|the architecture doc]].
```

**After:**
```markdown
See Overview for details.
Check out the architecture doc.
```

---

### 3. Private Block Removal

**Before:**
```markdown
Public content here.

<!-- private -->
Secret information that shouldn't be published.
Internal notes and TODOs.
<!-- /private -->

More public content.
```

**After:**
```markdown
Public content here.

More public content.
```

---

### 4. Image Path Transformation

**Before:**
```markdown
Screenshot: ![[screenshot.png]]
Diagram: ![[diagrams/architecture.png]]
```

**After:**
```markdown
Screenshot: ![screenshot](./images/screenshot.png)
Diagram: ![architecture](./images/architecture.png)
```

**Note:** This only transforms the syntax. Image file copying requires `images.copy: true` (not yet fully implemented).

---

## Exclusion Patterns

Protect sensitive files from being synced:

```yaml
exclude:
  # Exact match
  - ".env"
  - "secrets.md"

  # Wildcard patterns
  - "*.secret.md"
  - "*.private.*"

  # Directory patterns
  - "private/**"
  - "journals/**"
  - "drafts/*"
```

Exclusion patterns use Python's `fnmatch` for glob-style matching.

---

## Example Workflows

### Use Case 1: Project Documentation

**Goal:** Sync planning docs to public README

```yaml
vault_root: "/home/user/Obsidian/MyProject"
repo_root: "/home/user/Projects/my-project"

exclude:
  - "journals/**"
  - "*.private.md"

sync:
  - source: "PROJECT-OVERVIEW.md"
    dest: "README.md"
  - source: "ARCHITECTURE.md"
    dest: "docs/ARCHITECTURE.md"
  - source: "API-GUIDE.md"
    dest: "docs/API.md"
```

---

### Use Case 2: Blog Post Publishing

**Goal:** Publish blog posts while keeping drafts private

```yaml
vault_root: "/home/user/Obsidian/Blog"
repo_root: "/home/user/website/content/posts"

exclude:
  - "drafts/**"
  - "*.draft.md"
  - "ideas/**"

images:
  transform_paths: true
  dest_dir: "images"

sync:
  - source: "published/post-1.md"
    dest: "2026-01-25-my-post.md"
  - source: "published/post-2.md"
    dest: "2026-01-26-another-post.md"
```

---

## Testing

Run the test suite:

```bash
# All tests
pytest tests/test_transform.py tests/test_sync.py -v

# Just transformation tests
pytest tests/test_transform.py -v

# Just sync integration tests
pytest tests/test_sync.py -v
```

**Test Coverage:**
- 26 transformation unit tests
- 15 sync integration tests
- **41 total tests - all passing ✅**

---

## API Reference

### Functions

#### `sync_files(config_path: str, dry_run: bool = False)`

Main sync function.

**Parameters:**
- `config_path` (str): Path to `.jolly-sync.yaml` configuration file
- `dry_run` (bool): If True, show what would be synced without writing files

**Raises:**
- `ValueError`: If configuration is invalid or paths don't exist

**Example:**
```python
from jolly_flow.sync.sync import sync_files

# Normal sync
sync_files(".jolly-sync.yaml")

# Preview mode
sync_files(".jolly-sync.yaml", dry_run=True)
```

---

#### `is_excluded(file_path: str, exclusion_patterns: List[str]) -> bool`

Check if a file matches any exclusion pattern.

**Parameters:**
- `file_path` (str): Relative file path to check
- `exclusion_patterns` (List[str]): List of glob patterns

**Returns:**
- `bool`: True if file should be excluded

**Example:**
```python
from jolly_flow.sync.sync import is_excluded

patterns = ["*.secret.md", "private/**"]
is_excluded("data.secret.md", patterns)  # True
is_excluded("public.md", patterns)       # False
```

---

### Transformation Functions

#### `remove_frontmatter(content: str) -> str`

Remove YAML frontmatter from markdown.

---

#### `resolve_wikilinks(content: str) -> str`

Convert Obsidian wikilinks to plain text.

---

#### `remove_private_blocks(content: str) -> str`

Remove content between `<!-- private -->` tags.

---

#### `transform_image_paths(content: str, dest_images_dir: str = "images") -> str`

Convert Obsidian image syntax to standard markdown.

---

## Troubleshooting

### Issue: "Configuration missing required field: vault_root"

**Cause:** `.jolly-sync.yaml` is missing required fields

**Solution:** Ensure config has both `vault_root` and `repo_root`

---

### Issue: "Source not found: /path/to/file.md"

**Cause:** File listed in `sync` doesn't exist in vault

**Solution:** Check file path is correct and relative to `vault_root`

---

### Issue: Files not being excluded

**Cause:** Exclusion pattern doesn't match file path

**Solution:** Test pattern with `is_excluded()` function. Remember patterns are matched against relative paths from `vault_root`.

---

### Issue: Images not showing up in synced files

**Cause:** Image transformation changes syntax but doesn't copy files

**Solution:**
1. Ensure `images.transform_paths: true` in config
2. Image file copying is not yet implemented - copy manually or use separate script

---

## Known Limitations

1. **Image File Copying:** Syntax transformation works, but automatic image file copying is not yet implemented. Images must be copied manually.

2. **Nested Private Blocks:** Private blocks should not be nested. Behavior with nested blocks is undefined.

3. **One-Way Sync:** Sync is strictly vault → repo. Changes in repo are not synced back.

---

## Development

### Running Tests

```bash
# Install dev dependencies
uv pip install pytest

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=jolly_flow.sync
```

### Adding Transformations

1. Add function to `transform.py`
2. Add unit tests to `tests/test_transform.py`
3. Add integration test to `tests/test_sync.py`
4. Update configuration schema if needed
5. Document in this README

---

## Version History

- **0.1.0** (2026-01-25) - Phase 3 completion
  - Complete sync functionality
  - All transformations implemented
  - Exclusion patterns
  - Configuration validation
  - 41 tests all passing

---

## Related Documentation

- [Phase 3 Overview](/home/joseph/GoogleDrive/Obsidian/TheJollyMethod/guides/phase-3/overview.md)
- [Phase 3 Checklist](/home/joseph/GoogleDrive/Obsidian/TheJollyMethod/guides/phase-3/checklist.md)
- [.jolly-sync.yaml Schema](./SCHEMA.md)

---

**Part of The Jolly Method Framework** | **Phase 3 Complete ✅**
