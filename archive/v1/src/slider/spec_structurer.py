from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import List, Optional

from .spec import Deck, ImageRef, Slide


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_BULLET_RE = re.compile(r"^\s*[-*+]\s+(.+?)\s*$")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_CODE_FENCE_RE = re.compile(r"^\s*```")
_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")


def _truncate(text: str, max_chars: int) -> str:
    t = " ".join(text.strip().split())
    if len(t) <= max_chars:
        return t
    return t[: max(0, max_chars - 1)].rstrip() + "…"


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？.!?;；])\s+")
_VERSION_MARK_RE = re.compile(r"\bv\d+\s*[:：]")


def _split_by_version_markers(text: str) -> list[str]:
    matches = list(_VERSION_MARK_RE.finditer(text))
    if len(matches) < 2:
        return []
    parts: list[str] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        part = text[start:end].strip()
        if part:
            parts.append(part)
    return parts


def _wrap_no_loss(text: str, *, max_chars: int) -> list[str]:
    """
    Wrap long text into multiple chunks without deleting information.

    Uses punctuation/space boundaries when available; falls back to hard slicing.
    """

    t = " ".join(text.strip().split())
    if not t:
        return []
    if max_chars <= 0 or len(t) <= max_chars:
        return [t]

    boundaries = ["。", "！", "？", ".", "!", "?", "；", ";", "，", ",", " "]
    out: list[str] = []
    rest = t
    while len(rest) > max_chars:
        window = rest[:max_chars]
        cut = -1
        for b in boundaries:
            idx = window.rfind(b)
            if idx > cut:
                cut = idx
        if cut <= 0:
            cut = max_chars
        else:
            cut = cut + 1
        chunk = rest[:cut].strip()
        if chunk:
            out.append(chunk)
        rest = rest[cut:].strip()
        if not rest:
            break

    if rest:
        out.append(rest)

    if len(out) <= 1:
        return out
    # Mark continuation for readability.
    return [out[0]] + [f"（续）{c}" for c in out[1:]]


def _split_long_text_to_bullets(text: str, *, max_chars: int) -> list[str]:
    t = " ".join(text.strip().split())
    if not t:
        return []

    # Special-case common "v1: ... v2: ..." dense lists.
    version_parts = _split_by_version_markers(t)
    if version_parts:
        bullets: list[str] = []
        for part in version_parts:
            bullets.extend(_wrap_no_loss(part, max_chars=max_chars))
        return bullets

    # Split by sentence-ish boundaries first.
    sentence_parts = [p.strip() for p in _SENTENCE_SPLIT_RE.split(t) if p.strip()]
    if not sentence_parts:
        return _wrap_no_loss(t, max_chars=max_chars)

    bullets: list[str] = []
    for part in sentence_parts:
        bullets.extend(_wrap_no_loss(part, max_chars=max_chars))
    return bullets


def _paragraph_to_bullets(paragraph: str, *, max_chars: int) -> list[str]:
    # Preserve information: split into multiple bullets instead of truncating.
    return _split_long_text_to_bullets(paragraph, max_chars=max_chars)


def _chunk(items: List[str], size: int) -> List[List[str]]:
    if size <= 0:
        return [items]
    return [items[i : i + size] for i in range(0, len(items), size)]


@dataclass
class _Section:
    title: str
    bullets: List[str] = field(default_factory=list)
    paragraphs: List[str] = field(default_factory=list)
    images: List[ImageRef] = field(default_factory=list)
    raw_blocks: List[List[str]] = field(default_factory=list)


def _parse_material_markdown(text: str, *, deck_title: Optional[str], max_bullets_per_slide: int) -> Deck:
    deck = deck_title.strip() if deck_title else ""
    sections: List[_Section] = []
    current = _Section(title="")

    in_code_block = False
    code_block_lines: List[str] = []
    paragraph_lines: List[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            paragraph = " ".join([l.strip() for l in paragraph_lines if l.strip()])
            if paragraph:
                current.paragraphs.append(paragraph)
        paragraph_lines = []

    lines = text.splitlines()
    for raw in lines:
        line = raw.rstrip("\n")

        if _CODE_FENCE_RE.match(line):
            flush_paragraph()
            if not in_code_block:
                in_code_block = True
                code_block_lines = [line]
            else:
                in_code_block = False
                code_block_lines.append(line)
                current.raw_blocks.append(code_block_lines)
                code_block_lines = []
            continue
        if in_code_block:
            # Preserve code blocks (including empty lines).
            code_block_lines.append(line)
            continue

        if not line.strip():
            flush_paragraph()
            continue

        # Preserve markdown tables as-is.
        if _TABLE_ROW_RE.match(line) or _TABLE_SEP_RE.match(line):
            flush_paragraph()
            # Keep consecutive table lines in the same block.
            if current.raw_blocks and current.raw_blocks[-1] and (
                _TABLE_ROW_RE.match(current.raw_blocks[-1][-1]) or _TABLE_SEP_RE.match(current.raw_blocks[-1][-1])
            ):
                current.raw_blocks[-1].append(line)
            else:
                current.raw_blocks.append([line])
            continue

        # Extract image refs early. If the line is only images, do not turn it into a paragraph/bullet.
        images_in_line = _IMAGE_RE.findall(line)
        if images_in_line:
            for alt, src in images_in_line:
                current.images.append(ImageRef(alt=alt.strip(), src=src.strip()))
            # If removing all image markdown leaves no text, treat as "image-only" and skip content capture.
            remainder = _IMAGE_RE.sub("", line).strip()
            if not remainder:
                flush_paragraph()
                continue

        h = _HEADING_RE.match(line)
        if h:
            flush_paragraph()
            level = len(h.group(1))
            title = h.group(2).strip()
            if level == 1 and not deck:
                deck = title
                continue
            if level <= 3:
                if current.title or current.bullets or current.paragraphs or current.images:
                    sections.append(current)
                current = _Section(title=title)
                continue
            # Deeper headings become part of the paragraph flow.
            paragraph_lines.append(title)
            continue

        bullet = _BULLET_RE.match(line)
        if bullet:
            flush_paragraph()
            current.bullets.append(bullet.group(1).strip())
        else:
            paragraph_lines.append(line.strip())

        # Note: image refs are handled above to avoid duplicating image-only lines as bullets.

    flush_paragraph()
    if current.title or current.bullets or current.paragraphs or current.images:
        sections.append(current)

    if not deck:
        # Best-effort fallback: use the first non-empty line as title.
        for raw in lines:
            if raw.strip():
                deck = _truncate(raw.strip().lstrip("#").strip(), 60) or "Untitled Deck"
                break
        else:
            deck = "Untitled Deck"

    slides: List[Slide] = []
    if not sections:
        sections = [_Section(title=deck)]

    for section in sections:
        title = section.title.strip() or deck
        bullets: List[str] = []
        for b in section.bullets:
            if not b.strip():
                continue
            bullets.extend(_split_long_text_to_bullets(b, max_chars=120))
        for p in section.paragraphs:
            bullets.extend(_paragraph_to_bullets(p, max_chars=120))

        body_lines: List[str] = []
        for block in section.raw_blocks:
            if body_lines:
                body_lines.append("")
            body_lines.extend(block)

        if not bullets:
            # As a last resort, keep paragraphs as body lines.
            extra = [p for p in section.paragraphs if p.strip()]
            if extra:
                if body_lines:
                    body_lines.append("")
                body_lines.extend(extra)
            slides.append(Slide(title=title, body=body_lines, images=section.images))
            continue

        for idx, chunk in enumerate(_chunk(bullets, size=max_bullets_per_slide), start=1):
            slide_title = title if idx == 1 else f"{title} (cont.)"
            images = section.images if idx == 1 else []
            body = body_lines if idx == 1 else []
            slides.append(Slide(title=slide_title, bullets=chunk, body=body, images=images))

    return Deck(title=deck, slides=slides)


def structure_material_to_spec_markdown(
    text: str,
    *,
    deck_title: Optional[str] = None,
    max_bullets_per_slide: int = 6,
) -> str:
    """
    Convert unstructured Markdown material into a structured multi-slide SPEC (Markdown).

    Heuristics:
    - First H1 becomes deck title (unless overridden).
    - H2/H3 headings become slide/section boundaries.
    - Lists become bullets; paragraphs become 1 bullet (best-effort, truncated).
    - Fenced code blocks are ignored.
    - Slides are chunked to max_bullets_per_slide bullets each.
    """

    size = max_bullets_per_slide if max_bullets_per_slide > 0 else 6
    deck = _parse_material_markdown(text, deck_title=deck_title, max_bullets_per_slide=size)

    # Dump as SPEC markdown.
    out: list[str] = [f"# {deck.title}".rstrip(), ""]
    for slide in deck.slides:
        out.append(f"## {slide.title}".rstrip())
        if slide.bullets:
            for b in slide.bullets:
                out.append(f"- {b}".rstrip())
        if slide.body:
            if slide.bullets:
                out.append("")
            for line in slide.body:
                out.append(str(line).rstrip())
        if slide.images:
            if slide.bullets or slide.body:
                out.append("")
            for img in slide.images:
                out.append(f"![{img.alt}]({img.src})".rstrip())
        out.append("")
    return "\n".join(out).rstrip() + "\n"
