"""Tests for markdown metadata extraction."""

import tempfile
from pathlib import Path

from amplifier_module_markdown_utils import extract_title
from amplifier_module_markdown_utils import extract_title_from_file
from amplifier_module_markdown_utils import slugify


class TestExtractTitle:
    """Tests for extract_title function."""

    def test_extracts_h1_title(self):
        content = "# My Great Title\n\nSome content"
        assert extract_title(content) == "My Great Title"

    def test_extracts_first_h1_only(self):
        content = "# First Title\n\n# Second Title"
        assert extract_title(content) == "First Title"

    def test_handles_no_title(self):
        content = "## No H1 Here\n\nJust content"
        assert extract_title(content) is None

    def test_handles_empty_content(self):
        assert extract_title("") is None

    def test_handles_whitespace(self):
        content = "  # Title With Spaces  \n\nContent"
        assert extract_title(content) == "Title With Spaces"


class TestExtractTitleFromFile:
    """Tests for extract_title_from_file function."""

    def test_extracts_from_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test Title\n\nContent here")
            f.flush()
            path = Path(f.name)

        try:
            result = extract_title_from_file(path)
            assert result == "Test Title"
        finally:
            path.unlink()

    def test_handles_nonexistent_file(self):
        path = Path("/nonexistent/file.md")
        assert extract_title_from_file(path) is None


class TestSlugify:
    """Tests for slugify function."""

    def test_basic_slugification(self):
        assert slugify("Hello World") == "hello-world"

    def test_removes_special_chars(self):
        assert slugify("Hello & World!") == "hello-world"
        assert slugify("Test@123#456") == "test123456"

    def test_handles_multiple_spaces(self):
        assert slugify("Multiple   Spaces   Here") == "multiple-spaces-here"

    def test_handles_underscores(self):
        assert slugify("snake_case_text") == "snake-case-text"

    def test_removes_leading_trailing_dashes(self):
        assert slugify("  - Test - ") == "test"

    def test_handles_empty_string(self):
        assert slugify("") == ""

    def test_handles_numbers(self):
        assert slugify("Article 123 Test") == "article-123-test"

    def test_complex_example(self):
        assert slugify("The Quick & Brown Fox!!!") == "the-quick-brown-fox"
