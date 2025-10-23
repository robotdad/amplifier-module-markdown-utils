# amplifier-module-markdown-utils

**Markdown parsing, injection, and metadata extraction for Amplifier applications**

Process markdown documents with utilities for structure analysis, content injection, and metadata extraction.

---

## Installation

```bash
pip install git+https://github.com/robotdad/amplifier-dev#subdirectory=amplifier-module-markdown-utils
```

Or add to your `pyproject.toml`:

```toml
[tool.uv.sources.amplifier-module-markdown-utils]
git = "https://github.com/robotdad/amplifier-dev"
subdirectory = "amplifier-module-markdown-utils"
branch = "main"
```

---

## Quick Start

```python
from pathlib import Path
from amplifier_module_markdown_utils import (
    extract_title,
    slugify,
    MarkdownParser,
    MarkdownImageUpdater
)

# Simple operations
content = Path("article.md").read_text()
title = extract_title(content)
slug = slugify(title)  # "my-article-title"

# Structure analysis
parser = MarkdownParser()
doc = parser.parse(content)
print(f"Found {len(doc.sections)} sections")

# Image insertion
updater = MarkdownImageUpdater()
updated = updater.insert_image(
    content,
    "images/diagram.png",
    "System architecture",
    section_title="Architecture",
    placement="after_section"
)
```

---

## Features

- **Title Extraction**: Find first H1 heading in markdown
- **Slugification**: Convert titles to URL-friendly slugs
- **Structure Parsing**: Analyze sections, headings, content blocks
- **Image Insertion**: Add images at strategic positions
- **Metadata Extraction**: Pull frontmatter and document properties
- **Type Safety**: Full type hints throughout

---

## API Reference

### Simple Functions

```python
def extract_title(content: str) -> str | None:
    """Extract first H1 heading from markdown."""

def extract_title_from_file(path: Path) -> str | None:
    """Extract title from markdown file."""

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
```

### MarkdownParser

```python
class MarkdownParser:
    def parse(self, content: str) -> MarkdownDocument:
        """Parse markdown into structured representation."""

@dataclass
class MarkdownDocument:
    title: str | None
    sections: list[MarkdownSection]
    raw_content: str
```

### MarkdownImageUpdater

```python
class MarkdownImageUpdater:
    def insert_image(
        self,
        content: str,
        image_path: str,
        alt_text: str,
        *,
        placement: Literal["before_section", "after_section", "at_line"] = "at_line"
    ) -> str:
        """Insert image into markdown."""
```

---

## Usage Examples

See [examples/basic_usage.py](./examples/basic_usage.py) for complete examples.

---

## Integration with Amplifier

```python
# Register with coordinator
coordinator.register_capability("markdown.parser", parser)
coordinator.register_capability("markdown.metadata_extractor", extractor)

# Use in other modules
parser = coordinator.get_capability("markdown.parser")
if not parser:
    from amplifier_module_markdown_utils import MarkdownParser
    parser = MarkdownParser()
```

---

## Development

```bash
cd amplifier-module-markdown-utils
uv sync --dev
uv run pytest
```

---

## Learn More

- [HOW_THIS_MODULE_WAS_MADE.md](./HOW_THIS_MODULE_WAS_MADE.md)
- [examples/](./examples/)
- [Amplifier Documentation](https://github.com/microsoft/amplifier-dev/blob/main/docs/)
