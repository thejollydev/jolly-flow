import re

def remove_frontmatter(content: str) -> str:
    """Removes YAML frontmatter from markdown content."""
    return re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)

def resolve_wikilinks(content: str) -> str:
    """Converts Obsidian wikilinks [[Link|Text]] to Text or [[Link]] to Link."""
    def replace_link(match):
        target = match.group(1)
        text = match.group(2)
        return text if text else target

    return re.sub(r"\[\[(.*?)(?:\|(.*?))?\]\]", replace_link, content)
