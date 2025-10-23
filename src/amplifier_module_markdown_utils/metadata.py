"""Markdown metadata extraction utilities."""

import re
from pathlib import Path


def extract_title(content: str) -> str | None:
    """Extract the first H1 heading from markdown content.

    Args:
        content: Markdown content

    Returns:
        Title string or None if no title found

    Examples:
        >>> extract_title("# Hello World\\nSome content")
        'Hello World'
        >>> extract_title("No title here")
        None
    """
    lines = content.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def extract_title_from_file(path: Path) -> str | None:
    """Extract title from a markdown file.

    Args:
        path: Path to markdown file

    Returns:
        Title string or None if no title found or file doesn't exist

    Examples:
        >>> from pathlib import Path
        >>> # Assuming file exists with title
        >>> title = extract_title_from_file(Path("article.md"))
    """
    try:
        content = path.read_text(encoding="utf-8")
        return extract_title(content)
    except OSError:
        return None


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified string (lowercase, dashes for spaces, no special chars)

    Examples:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("This & That")
        'this-that'
        >>> slugify("Multiple   Spaces")
        'multiple-spaces'
    """
    slug = text.lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug
