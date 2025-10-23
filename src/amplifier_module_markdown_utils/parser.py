"""Markdown parsing utilities."""

from pathlib import Path

from .models import MarkdownDocument
from .models import MarkdownSection


class MarkdownParser:
    """Parses markdown documents into structured representation."""

    def parse(self, content: str) -> MarkdownDocument:
        """Parse markdown content into structured document.

        Args:
            content: Markdown content to parse

        Returns:
            Structured markdown document with sections

        Examples:
            >>> parser = MarkdownParser()
            >>> doc = parser.parse("# Title\\n\\nContent here\\n\\n## Section\\n\\nMore content")
            >>> doc.title
            'Title'
            >>> len(doc.sections)
            1
        """
        lines = content.split("\n")
        sections: list[MarkdownSection] = []
        current_section: dict[str, object] = {}

        title = None

        for line_num, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith("# ") and title is None:
                title = stripped[2:].strip()
                continue

            if stripped.startswith("## "):
                if current_section:
                    sections.append(self._finalize_section(current_section))

                current_section = {
                    "title": stripped[3:].strip(),
                    "level": 2,
                    "line_number": line_num,
                    "content_lines": [line],
                }
            elif stripped.startswith("### "):
                if current_section:
                    sections.append(self._finalize_section(current_section))

                current_section = {
                    "title": stripped[4:].strip(),
                    "level": 3,
                    "line_number": line_num,
                    "content_lines": [line],
                }
            elif current_section:
                content_lines = current_section.get("content_lines", [])
                if isinstance(content_lines, list):
                    content_lines.append(line)

        if current_section:
            sections.append(self._finalize_section(current_section))

        return MarkdownDocument(
            raw_content=content,
            title=title,
            sections=sections,
        )

    def parse_file(self, path: Path) -> MarkdownDocument:
        """Parse markdown file into structured document.

        Args:
            path: Path to markdown file

        Returns:
            Structured markdown document

        Examples:
            >>> parser = MarkdownParser()
            >>> doc = parser.parse_file(Path("article.md"))
        """
        content = path.read_text(encoding="utf-8")
        return self.parse(content)

    def _finalize_section(self, section_data: dict) -> MarkdownSection:
        """Convert section data dict to MarkdownSection.

        Args:
            section_data: Section data dictionary

        Returns:
            MarkdownSection object
        """
        content_lines = section_data["content_lines"]
        if not isinstance(content_lines, list):
            content_lines = []

        return MarkdownSection(
            title=str(section_data["title"]),
            level=int(section_data["level"]),
            line_number=int(section_data["line_number"]),
            content="\n".join(content_lines),
        )
