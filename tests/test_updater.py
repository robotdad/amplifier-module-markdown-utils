"""Tests for markdown updater."""

import tempfile
from pathlib import Path

from amplifier_module_markdown_utils import MarkdownImageUpdater


class TestMarkdownImageUpdater:
    """Tests for MarkdownImageUpdater class."""

    def test_inserts_image_at_line(self):
        content = "# Title\n\nLine 1\nLine 2\nLine 3"
        updater = MarkdownImageUpdater()

        result = updater.insert_image(content, line_number=3, image_path="images/test.png", alt_text="Test Image")

        assert "images/test.png" in result
        assert 'alt="Test Image"' in result
        assert '<img src="images/test.png"' in result

    def test_inserts_with_width(self):
        content = "# Title\n\nContent"
        updater = MarkdownImageUpdater()

        result = updater.insert_image(
            content, line_number=2, image_path="images/test.png", alt_text="Test", width="75%"
        )

        assert 'width="75%"' in result

    def test_inserts_without_width(self):
        content = "# Title\n\nContent"
        updater = MarkdownImageUpdater()

        result = updater.insert_image(content, line_number=2, image_path="images/test.png", alt_text="Test", width=None)

        assert "![Test](images/test.png)" in result
        assert "width=" not in result

    def test_before_section_placement(self):
        content = "# Title\n\nIntro\n\n## Section\n\nSection content"
        updater = MarkdownImageUpdater()

        result = updater.insert_image(
            content, line_number=4, image_path="images/test.png", alt_text="Test", placement="before_section"
        )

        lines = result.split("\n")
        section_line = next(i for i, line in enumerate(lines) if "## Section" in line)
        image_line = next(i for i, line in enumerate(lines) if "images/test.png" in line)

        assert image_line < section_line

    def test_after_intro_placement(self):
        content = "# Title\n\nIntro paragraph\n\nNext paragraph"
        updater = MarkdownImageUpdater()

        result = updater.insert_image(
            content, line_number=2, image_path="images/test.png", alt_text="Test", placement="after_intro"
        )

        assert "Intro paragraph" in result
        assert "images/test.png" in result

    def test_insert_image_in_file(self):
        content = "# Title\n\nContent here\n\n## Section"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as input_file:
            input_file.write(content)
            input_file.flush()
            input_path = Path(input_file.name)

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as output_file:
            output_path = Path(output_file.name)

        try:
            updater = MarkdownImageUpdater()
            updater.insert_image_in_file(
                input_path, output_path, line_number=3, image_path="images/pic.png", alt_text="Picture"
            )

            result = output_path.read_text(encoding="utf-8")
            assert "images/pic.png" in result
            assert "Picture" in result
        finally:
            input_path.unlink()
            if output_path.exists():
                output_path.unlink()

    def test_handles_boundary_conditions(self):
        content = "Line 1\nLine 2"
        updater = MarkdownImageUpdater()

        result = updater.insert_image(content, line_number=0, image_path="images/start.png", alt_text="Start")
        assert "images/start.png" in result

        result = updater.insert_image(content, line_number=10, image_path="images/end.png", alt_text="End")
        assert "images/end.png" in result
