from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable, List, Optional, Sequence


_H1_RE = re.compile(r"^#\s+(.+?)\s*$")
_H2_RE = re.compile(r"^##\s+(.+?)\s*$")
_BULLET_RE = re.compile(r"^\s*[-*+]\s+(.+?)\s*$")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_CODE_FENCE_RE = re.compile(r"^\s*```")


@dataclass
class ImageRef:
    alt: str
    src: str


@dataclass
class Slide:
    title: str
    bullets: List[str] = field(default_factory=list)
    body: List[str] = field(default_factory=list)
    images: List[ImageRef] = field(default_factory=list)


@dataclass
class Deck:
    title: str
    slides: List[Slide]


def parse_markdown_spec(text: str) -> Deck:
    deck_title = "Untitled Deck"
    slides: List[Slide] = []
    current: Optional[Slide] = None
    in_code_block = False

    lines = text.splitlines()
    for raw in lines:
        line = raw.rstrip("\n")

        if _CODE_FENCE_RE.match(line):
            if current is None:
                current = Slide(title=deck_title)
                slides.append(current)
            current.body.append(line.rstrip())
            in_code_block = not in_code_block
            continue

        if in_code_block:
            if current is None:
                current = Slide(title=deck_title)
                slides.append(current)
            # Preserve code block content verbatim, including blank lines.
            current.body.append(line.rstrip())
            continue

        if not line.strip():
            continue

        h1 = _H1_RE.match(line)
        if h1 and (deck_title == "Untitled Deck"):
            deck_title = h1.group(1).strip()
            continue

        h2 = _H2_RE.match(line)
        if h2:
            current = Slide(title=h2.group(1).strip())
            slides.append(current)
            continue

        if current is None:
            current = Slide(title=deck_title)
            slides.append(current)

        # Preserve markdown tables as body; avoid treating their rows as bullets.
        if line.lstrip().startswith("|"):
            current.body.append(line.strip())
            continue

        bullet = _BULLET_RE.match(line)
        if bullet:
            current.bullets.append(bullet.group(1).strip())
        else:
            current.body.append(line.strip())

        for alt, src in _IMAGE_RE.findall(line):
            current.images.append(ImageRef(alt=alt.strip(), src=src.strip()))

    if not slides:
        slides = [Slide(title=deck_title)]
    return Deck(title=deck_title, slides=slides)


def infer_layout(slide: Slide) -> str:
    if slide.images:
        # If the slide is primarily an image with at most a tiny caption, prefer full-bleed.
        if (not slide.body) and (len(slide.bullets) <= 1):
            return "image_full_bleed_caption"
        if slide.bullets or slide.body:
            return "image_left_text_right"
        return "image_full_bleed_caption"
    has_code = any("```" in line for line in slide.body)
    has_table = any(line.lstrip().startswith("|") for line in slide.body)
    if has_code:
        return "title_bullets_code" if slide.bullets else "title_code"
    if has_table:
        return "title_bullets_table" if slide.bullets else "title_table"
    bullet_count = len(slide.bullets)
    if bullet_count >= 7:
        return "two_column_bullets"
    if bullet_count >= 1:
        return "title_bullets"
    return "title_only"
