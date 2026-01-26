# jolly-flow Sync

Documentation-to-Repository Synchronization Engine.

The `sync` module handles the transformation of Obsidian-flavored Markdown into standard Markdown suitable for public Git repositories.

## Features

- **Wikilink Resolution:** Converts `[[Links]]` to plain text.
- **Frontmatter Sanitization:** Removes YAML frontmatter used by Obsidian plugins.
- **Private Block Removal:** Deletes content wrapped in `<!-- private -->` tags.
- **Image Path Normalization:** Resolves `![[image.png]]` to standard `![](path/to/image.png)`.
- **Exclusion Patterns:** Supports glob matching to exclude journals, templates, or private notes.

## Configuration

Sync is controlled by a `.jolly-sync.yaml` file in the project root.

```yaml
# Example configuration
source_dir: "/path/to/obsidian/vault"
target_dir: "/path/to/git/repo"
transformations:
  remove_frontmatter: true
  resolve_wikilinks: true
  remove_private_blocks: true
  fix_image_paths: true
exclude:
  - "journals/**"
  - "templates/**"
  - "*.private.md"
```

## Usage

```bash
jolly-flow sync --config .jolly-sync.yaml
```

Use `--dry-run` to preview changes without writing any files.
