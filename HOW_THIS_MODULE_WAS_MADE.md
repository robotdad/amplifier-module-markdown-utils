# How This Module Was Made

**Consolidation of markdown utilities from blog_writer and article_illustrator**

---

## The Problem

Both scenario tools processed markdown but implemented their own utilities:
- blog_writer: Title extraction, slugification
- article_illustrator: Structure parsing, image insertion, content analysis

This duplication meant:
- Other apps couldn't reuse these utilities
- No consistency across tools
- Missed opportunity for shared module

---

## The Solution: Consolidate as Reusable Module

**What We Extracted**:
- From blog_writer: `extract_title_from_markdown()`, `slugify()`
- From article_illustrator: `MarkdownParser`, `MarkdownImageUpdater`, structure analysis

**Total**: ~400 LOC consolidated from two sources

---

## Design Decisions

### Decision 1: Functions vs Classes
**Chose**: Functions for simple ops (extract, slugify), classes for complex (parse, update)
**Why**: Simpler interface, no unnecessary classes

### Decision 2: No Async
**Chose**: Synchronous interface
**Why**: Markdown processing is CPU-bound, not I/O

### Decision 3: Flexible Placement
**Chose**: Support multiple placement strategies (before/after section, at line)
**Why**: Different use cases need different insertion logic

---

## Reusability

Use cases:
- Blog post formatters
- Documentation generators
- README creators
- Wiki page builders
- Any markdown manipulation

---

**Created**: 2025-10-22
**Consolidated From**: scenarios/blog_writer + article_illustrator
**Status**: Active development
