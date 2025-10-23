"""Tests for markdown parser."""

import tempfile
from pathlib import Path

from amplifier_module_markdown_utils import MarkdownParser


class TestMarkdownParser:
    """Tests for MarkdownParser class."""

    def test_parses_simple_document(self):
        content = "# Main Title\n\nIntro text\n\n## Section One\n\nSection content"
        parser = MarkdownParser()
        doc = parser.parse(content)

        assert doc.title == "Main Title"
        assert len(doc.sections) == 1
        assert doc.sections[0].title == "Section One"
        assert doc.sections[0].level == 2

    def test_parses_multiple_sections(self):
        content = """# Document Title

Intro paragraph

## First Section

First content

## Second Section

Second content

### Subsection

Sub content"""
        parser = MarkdownParser()
        doc = parser.parse(content)

        assert doc.title == "Document Title"
        assert len(doc.sections) == 3
        assert doc.sections[0].title == "First Section"
        assert doc.sections[1].title == "Second Section"
        assert doc.sections[2].title == "Subsection"
        assert doc.sections[2].level == 3

    def test_handles_no_title(self):
        content = "## Just a section\n\nNo H1 title"
        parser = MarkdownParser()
        doc = parser.parse(content)

        assert doc.title is None
        assert len(doc.sections) == 1

    def test_handles_empty_content(self):
        content = ""
        parser = MarkdownParser()
        doc = parser.parse(content)

        assert doc.title is None
        assert len(doc.sections) == 0

    def test_preserves_raw_content(self):
        content = "# Title\n\n## Section"
        parser = MarkdownParser()
        doc = parser.parse(content)

        assert doc.raw_content == content

    def test_parse_file(self):
        content = "# File Title\n\n## File Section\n\nFile content"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            f.flush()
            path = Path(f.name)

        try:
            parser = MarkdownParser()
            doc = parser.parse_file(path)

            assert doc.title == "File Title"
            assert len(doc.sections) == 1
            assert doc.sections[0].title == "File Section"
        finally:
            path.unlink()

    def test_tracks_line_numbers(self):
        content = """# Title

Line 2

## Section One
Line 5
Line 6

## Section Two
Line 9"""
        parser = MarkdownParser()
        doc = parser.parse(content)

        assert doc.sections[0].line_number == 4
        assert doc.sections[1].line_number == 8

    def test_captures_section_content(self):
        content = "# Title\n\n## Section\nLine 1\nLine 2"
        parser = MarkdownParser()
        doc = parser.parse(content)

        assert "## Section" in doc.sections[0].content
        assert "Line 1" in doc.sections[0].content
        assert "Line 2" in doc.sections[0].content
