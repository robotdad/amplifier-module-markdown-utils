"""Tests for markdown models."""

import pytest
from amplifier_module_markdown_utils.models import MarkdownDocument
from amplifier_module_markdown_utils.models import MarkdownError
from amplifier_module_markdown_utils.models import MarkdownInsertError
from amplifier_module_markdown_utils.models import MarkdownParseError
from amplifier_module_markdown_utils.models import MarkdownSection


def test_markdown_section_creation():
    """Test creating a MarkdownSection."""
    section = MarkdownSection(
        title="Introduction",
        level=2,
        line_number=5,
        content="## Introduction\n\nThis is the intro paragraph.",
    )

    assert section.title == "Introduction"
    assert section.level == 2
    assert section.line_number == 5
    assert "## Introduction" in section.content
    assert "intro paragraph" in section.content


def test_markdown_section_h1():
    """Test MarkdownSection for H1 heading."""
    section = MarkdownSection(
        title="Main Title",
        level=1,
        line_number=1,
        content="# Main Title\n\nDocument content.",
    )

    assert section.title == "Main Title"
    assert section.level == 1
    assert section.line_number == 1


def test_markdown_section_different_levels():
    """Test MarkdownSection with different heading levels."""
    for level in range(1, 7):
        section = MarkdownSection(
            title=f"Heading Level {level}",
            level=level,
            line_number=10,
            content=f"{'#' * level} Heading Level {level}\n\nContent.",
        )

        assert section.level == level
        assert section.title == f"Heading Level {level}"


def test_markdown_document_creation():
    """Test creating a MarkdownDocument."""
    sections = [
        MarkdownSection("My Article", 1, 1, "# My Article\n\nIntroduction text."),
        MarkdownSection("Section One", 2, 5, "## Section One\n\nSection content."),
        MarkdownSection("Section Two", 2, 10, "## Section Two\n\nMore content."),
    ]

    doc = MarkdownDocument(
        title="My Article",
        sections=sections,
        raw_content="# My Article\n\nIntroduction text.\n\n## Section One\n\nSection content.\n\n## Section Two\n\nMore content.",
    )

    assert doc.title == "My Article"
    assert len(doc.sections) == 3
    assert doc.sections[0].title == "My Article"
    assert doc.sections[1].title == "Section One"
    assert doc.sections[2].title == "Section Two"


def test_markdown_document_no_title():
    """Test MarkdownDocument with no title (no H1)."""
    sections = [
        MarkdownSection("Introduction", 2, 1, "## Introduction\n\nContent."),
        MarkdownSection("Details", 2, 5, "## Details\n\nMore content."),
    ]

    doc = MarkdownDocument(
        title=None,
        sections=sections,
        raw_content="## Introduction\n\nContent.\n\n## Details\n\nMore content.",
    )

    assert doc.title is None
    assert len(doc.sections) == 2


def test_markdown_document_empty_sections():
    """Test MarkdownDocument with no sections."""
    doc = MarkdownDocument(title=None, sections=[], raw_content="Just plain text, no headings.")

    assert doc.title is None
    assert len(doc.sections) == 0
    assert doc.raw_content == "Just plain text, no headings."


def test_markdown_document_nested_sections():
    """Test MarkdownDocument with nested section hierarchy."""
    sections = [
        MarkdownSection("Main", 1, 1, "# Main"),
        MarkdownSection("Subsection", 2, 3, "## Subsection"),
        MarkdownSection("Sub-subsection", 3, 5, "### Sub-subsection"),
    ]

    doc = MarkdownDocument(
        title="Main",
        sections=sections,
        raw_content="# Main\n\n## Subsection\n\n### Sub-subsection",
    )

    assert len(doc.sections) == 3
    assert doc.sections[0].level == 1
    assert doc.sections[1].level == 2
    assert doc.sections[2].level == 3


def test_markdown_document_preserves_raw_content():
    """Test that MarkdownDocument preserves original content."""
    original = (
        "# Title\n\nSome **bold** and *italic* text.\n\n- List item 1\n- List item 2\n\n```python\ncode_block()\n```"
    )

    doc = MarkdownDocument(title="Title", sections=[], raw_content=original)

    assert doc.raw_content == original


def test_markdown_error_hierarchy():
    """Test exception hierarchy for markdown errors."""
    assert issubclass(MarkdownParseError, MarkdownError)
    assert issubclass(MarkdownInsertError, MarkdownError)


def test_markdown_error_raising():
    """Test that markdown errors can be raised and caught."""
    with pytest.raises(MarkdownError):
        raise MarkdownParseError("Parse failed")

    with pytest.raises(MarkdownError):
        raise MarkdownInsertError("Insert failed")


def test_markdown_section_line_numbers():
    """Test that section line numbers are tracked correctly."""
    sections = [
        MarkdownSection("Title", 1, 1, "# Title"),
        MarkdownSection("Intro", 2, 3, "## Intro"),
        MarkdownSection("Body", 2, 10, "## Body"),
        MarkdownSection("Conclusion", 2, 25, "## Conclusion"),
    ]

    doc = MarkdownDocument(title="Title", sections=sections, raw_content="content")

    assert doc.sections[0].line_number == 1
    assert doc.sections[1].line_number == 3
    assert doc.sections[2].line_number == 10
    assert doc.sections[3].line_number == 25


def test_markdown_section_multiline_content():
    """Test MarkdownSection with multiline content."""
    content = """## Introduction

This is a paragraph.

This is another paragraph with **bold** text.

- List item 1
- List item 2
"""
    section = MarkdownSection(title="Introduction", level=2, line_number=1, content=content)

    assert section.title == "Introduction"
    assert "paragraph" in section.content
    assert "**bold**" in section.content
    assert "List item 1" in section.content
