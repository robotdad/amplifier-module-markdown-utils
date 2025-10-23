"""Amplifier module for markdown parsing and manipulation."""

from .metadata import extract_title
from .metadata import extract_title_from_file
from .metadata import slugify
from .models import MarkdownDocument
from .models import MarkdownError
from .models import MarkdownInsertError
from .models import MarkdownParseError
from .models import MarkdownSection
from .parser import MarkdownParser
from .updater import MarkdownImageUpdater

__version__ = "0.1.0"

__all__ = [
    "extract_title",
    "extract_title_from_file",
    "slugify",
    "MarkdownDocument",
    "MarkdownSection",
    "MarkdownError",
    "MarkdownParseError",
    "MarkdownInsertError",
    "MarkdownParser",
    "MarkdownImageUpdater",
]
