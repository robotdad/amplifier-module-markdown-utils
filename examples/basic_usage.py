"""Basic usage examples for amplifier-module-markdown-utils."""

from pathlib import Path

from amplifier_module_markdown_utils import MarkdownImageUpdater
from amplifier_module_markdown_utils import MarkdownParser
from amplifier_module_markdown_utils import extract_title
from amplifier_module_markdown_utils import slugify


def example_title_and_slug():
    """Extract title and create slug."""
    content = Path("article.md").read_text()

    title = extract_title(content)
    if title:
        slug = slugify(title)
        print(f"Title: {title}")
        print(f"Slug: {slug}")


def example_parse_structure():
    """Parse markdown structure."""
    content = Path("article.md").read_text()

    parser = MarkdownParser()
    doc = parser.parse(content)

    print(f"Title: {doc.title}")
    print(f"Sections: {len(doc.sections)}")
    for section in doc.sections[:3]:
        print(f"  - {section.title} (level {section.level})")


def example_insert_image():
    """Insert image into markdown."""
    content = Path("article.md").read_text()

    updater = MarkdownImageUpdater()
    updated = updater.insert_image(
        content,
        "images/architecture.png",
        "System architecture diagram",
        section_title="Architecture Overview",
        placement="after_section",
    )

    print("Image inserted after 'Architecture Overview' section")
    Path("updated_article.md").write_text(updated)


if __name__ == "__main__":
    print("=== Title and Slug ===")
    example_title_and_slug()

    print("\n=== Parse Structure ===")
    example_parse_structure()

    print("\n=== Insert Image ===")
    example_insert_image()
