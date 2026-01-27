from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Iterable, List, Optional, Sequence


_H1_RE = re.compile(r"^#\s+(.+?)\s*$")
_H2_RE = re.compile(r"^##\s+(.+?)\s*$")
_BULLET_RE = re.compile(r"^\s*[-*+]\s+(.+?)\s*$")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


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

    lines = text.splitlines()
    for raw in lines:
        line = raw.rstrip("\n")
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
        if slide.bullets or slide.body:
            return "image_left_text_right"
        return "image_full_bleed_caption"
    bullet_count = len(slide.bullets)
    if bullet_count >= 7:
        return "two_column_bullets"
    if bullet_count >= 1:
        return "title_bullets"
    return "title_only"

