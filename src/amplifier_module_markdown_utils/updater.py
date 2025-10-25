"""Markdown content update utilities."""

from pathlib import Path


class MarkdownImageUpdater:
    """Updates markdown files by inserting images at specified locations."""

    def insert_image(
        self,
        content: str,
        line_number: int | None,
        image_path: str,
        alt_text: str = "",
        width: str | None = "50%",
        placement: str = "at_line",
    ) -> str:
        """Insert an image into markdown content.

        Args:
            content: Original markdown content
            line_number: Target line number for insertion
            image_path: Relative path to image file
            alt_text: Alt text for image
            width: Optional width attribute (HTML img tag)
            placement: Insertion strategy - "at_line", "before_section", "after_intro"

        Returns:
            Updated markdown content

        Examples:
            >>> updater = MarkdownImageUpdater()
            >>> content = "# Title\\n\\nContent here\\n\\n## Section\\n\\nMore content"
            >>> updated = updater.insert_image(content, 4, "images/pic.png", "My pic")
            >>> "img src" in updated
            True
        """
        lines = content.split("\n")

        image_markdown = self._create_image_markdown(image_path, alt_text, width)

        insert_line = self._find_insertion_line(lines, line_number, placement)

        if 0 <= insert_line <= len(lines):
            lines.insert(insert_line, image_markdown)

        return "\n".join(lines)

    def insert_image_in_file(
        self,
        input_path: Path,
        output_path: Path,
        line_number: int,
        image_path: str,
        alt_text: str = "",
        width: str | None = "50%",
        placement: str = "at_line",
    ) -> None:
        """Insert an image into a markdown file.

        Args:
            input_path: Path to input markdown file
            output_path: Path to output markdown file
            line_number: Target line number for insertion
            image_path: Relative path to image file
            alt_text: Alt text for image
            width: Optional width attribute
            placement: Insertion strategy

        Examples:
            >>> updater = MarkdownImageUpdater()
            >>> updater.insert_image_in_file(
            ...     Path("input.md"),
            ...     Path("output.md"),
            ...     5,
            ...     "images/pic.png",
            ...     "My picture"
            ... )
        """
        content = input_path.read_text(encoding="utf-8")
        updated = self.insert_image(content, line_number, image_path, alt_text, width, placement)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(updated, encoding="utf-8")

    def _create_image_markdown(self, image_path: str, alt_text: str, width: str | None) -> str:
        """Create markdown/HTML for image.

        Args:
            image_path: Path to image
            alt_text: Alt text
            width: Optional width attribute

        Returns:
            Image markdown string
        """
        if width:
            return f'\n<img src="{image_path}" alt="{alt_text}" width="{width}">\n'
        return f"\n![{alt_text}]({image_path})\n"

    def _find_insertion_line(self, lines: list[str], target: int | None, placement: str) -> int:
        """Find the best line to insert content.

        Args:
            lines: Content lines
            target: Target line number (None = auto-determine)
            placement: Insertion strategy

        Returns:
            Line index for insertion
        """
        # If no target specified, use middle of document
        if target is None:
            target = len(lines) // 2

        if placement == "before_section":
            for i in range(max(0, target - 5), min(len(lines), target + 5)):
                if i < len(lines) and lines[i].startswith("##"):
                    return i

        elif placement == "after_intro":
            for i in range(target, min(len(lines), target + 20)):
                if i < len(lines) and not lines[i].strip() and i > target:
                    return i + 1

        return min(target, len(lines))
