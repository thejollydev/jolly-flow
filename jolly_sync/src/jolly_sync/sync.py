import os
import yaml
from .transform import remove_frontmatter, resolve_wikilinks

def sync_files(config_path: str, dry_run: bool = False):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    vault_root = config.get("vault_root")
    repo_root = config.get("repo_root")
    sync_list = config.get("sync", [])

    for item in sync_list:
        source_rel = item.get("source")
        dest_rel = item.get("dest")

        source_path = os.path.join(vault_root, source_rel)
        dest_path = os.path.join(repo_root, dest_rel)

        if not os.path.exists(source_path):
            print(f"⚠️ Source not found: {source_path}")
            continue

        print(f"🔄 Syncing: {source_rel} -> {dest_rel}")

        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Apply transformations
        content = remove_frontmatter(content)
        content = resolve_wikilinks(content)

        if not dry_run:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Written: {dest_path}")
        else:
            print(f"  🔍 Dry run: would write to {dest_path}")
