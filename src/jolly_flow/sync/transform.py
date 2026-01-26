import re

def remove_frontmatter(content: str) -> str:
    """
    Removes YAML frontmatter from markdown content.

    Args:
        content: Markdown content with optional frontmatter

    Returns:
        Content with frontmatter removed

    Example:
        >>> remove_frontmatter("---\\ntitle: Test\\n---\\nContent")
        'Content'
    """
    # Match frontmatter with zero or more characters between delimiters
    return re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL)

def resolve_wikilinks(content: str) -> str:
    """
    Converts Obsidian wikilinks to plain text.

    Transforms:
    - [[Link|Text]] → Text
    - [[Link]] → Link

    Does NOT match image syntax (![[...]]) which should be handled by transform_image_paths.

    Args:
        content: Markdown content with Obsidian wikilinks

    Returns:
        Content with wikilinks converted to plain text

    Example:
        >>> resolve_wikilinks("See [[Overview|this page]]")
        'See this page'
        >>> resolve_wikilinks("See [[Overview]]")
        'See Overview'
    """
    def replace_link(match):
        target = match.group(1)
        text = match.group(2)
        return text if text else target

    # Use negative lookbehind to NOT match if preceded by !
    return re.sub(r"(?<!!)\[\[(.*?)(?:\|(.*?))?\]\]", replace_link, content)

def remove_private_blocks(content: str) -> str:
    """
    Removes content between <!-- private --> and <!-- /private --> tags.

    This allows marking sections of documents as private while keeping
    the rest public-facing.

    Args:
        content: Markdown content with optional private blocks

    Returns:
        Content with private blocks removed

    Example:
        >>> remove_private_blocks("Public\\n<!-- private -->Secret<!-- /private -->\\nPublic")
        'Public\\n\\nPublic'
    """
    return re.sub(r"<!--\s*private\s*-->.*?<!--\s*/private\s*-->", "", content, flags=re.DOTALL | re.IGNORECASE)

def transform_image_paths(content: str, dest_images_dir: str = "images") -> str:
    """
    Transforms Obsidian image syntax to standard markdown.

    Transforms:
    - ![[image.png]] → ![image](./images/image.png)
    - ![[folder/image.png]] → ![image](./images/image.png)

    Args:
        content: Markdown content with Obsidian image syntax
        dest_images_dir: Destination directory for images (relative path)

    Returns:
        Content with standard markdown image syntax

    Example:
        >>> transform_image_paths("![[screenshot.png]]")
        '![screenshot](./images/screenshot.png)'
    """
    def replace_image(match):
        image_path = match.group(1)
        # Extract just the filename (remove any path components)
        image_name = image_path.split("/")[-1]
        # Remove extension for alt text
        alt_text = image_name.rsplit(".", 1)[0]
        return f"![{alt_text}](./{dest_images_dir}/{image_name})"

    return re.sub(r"!\[\[(.*?)\]\]", replace_image, content)
