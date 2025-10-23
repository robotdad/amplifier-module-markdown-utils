"""Data models for markdown operations."""

from dataclasses import dataclass


class MarkdownError(Exception):
    """Base exception for markdown operations."""


class MarkdownParseError(MarkdownError):
    """Raised when markdown parsing fails."""


class MarkdownInsertError(MarkdownError):
    """Raised when markdown insertion fails."""


@dataclass
class MarkdownSection:
    """A section of a markdown document identified by a heading.

    Represents a logical section in a markdown document, starting with
    a heading and containing all content until the next heading of the
    same or higher level.

    Attributes:
        title: The heading text (without # markers)
        level: Heading level (1-6, where 1 is H1, 2 is H2, etc.)
        line_number: Line number where this section starts (1-indexed)
        content: Full content of the section including the heading

    Example:
        >>> section = MarkdownSection(
        ...     title="Introduction",
        ...     level=2,
        ...     line_number=5,
        ...     content="## Introduction\\n\\nThis is the intro paragraph."
        ... )
        >>> assert section.title == "Introduction"
        >>> assert section.level == 2
        >>> assert section.line_number == 5
    """

    title: str
    level: int
    line_number: int
    content: str


@dataclass
class MarkdownDocument:
    """Structured representation of a parsed markdown document.

    Represents a markdown document as a collection of sections with
    metadata about the document structure.

    Attributes:
        title: Document title (first H1 heading), None if no H1 found
        sections: List of sections in the document
        raw_content: Original unparsed markdown content

    Example:
        >>> doc = MarkdownDocument(
        ...     title="My Article",
        ...     sections=[
        ...         MarkdownSection("My Article", 1, 1, "# My Article"),
        ...         MarkdownSection("Introduction", 2, 3, "## Introduction\\n\\nText here.")
        ...     ],
        ...     raw_content="# My Article\\n\\n## Introduction\\n\\nText here."
        ... )
        >>> assert doc.title == "My Article"
        >>> assert len(doc.sections) == 2
        >>> assert doc.sections[0].level == 1
        >>> assert doc.sections[1].level == 2
    """

    title: str | None
    sections: list[MarkdownSection]
    raw_content: str
