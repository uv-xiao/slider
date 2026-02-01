#!/usr/bin/env python3
from __future__ import annotations

"""
Generate an *editable* PPTX from v2 styled prompts by reading a machine-readable
element inventory embedded in each slide block.

Expected per-slide structure in prompts/styled/*.md:

## Slide N: Title
...
```json
{
  "elements": [
    {
      "id": "title",
      "type": "title",
      "bbox_pct": [8, 8, 84, 12],
      "text": "My Title",
      "style": {"font_size": 40, "bold": true, "color": "#111111", "align": "left"}
    }
  ]
}
```

Notes:
- bbox_pct uses [x, y, w, h] in percent of the slide canvas (top-left origin).
- This generator focuses on editable text, simple shapes, and basic tables.
- Complex visuals (illustrations/diagrams) should be embedded as images or left
  to the image-based PPTX mode.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

try:
    from pptx import Presentation  # type: ignore[import-not-found]
    from pptx.dml.color import RGBColor  # type: ignore[import-not-found]
    from pptx.enum.text import PP_ALIGN  # type: ignore[import-not-found]
    from pptx.util import Inches, Pt  # type: ignore[import-not-found]
except ImportError:
    print("Error: python-pptx not found. Install with: pip install python-pptx", file=sys.stderr)
    raise SystemExit(1)


_SLIDE_HEADER_RE = re.compile(r"^##\s+Slide\s+(\d+):\s+(.+?)\s*$", re.M)
_JSON_FENCE_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S | re.I)


@dataclass(frozen=True)
class SlideBlock:
    index: int
    title: str
    block: str


def _hex_to_rgb(value: str) -> Optional[RGBColor]:
    v = (value or "").strip()
    if not v:
        return None
    if v.startswith("#"):
        v = v[1:]
    if len(v) != 6:
        return None
    try:
        r = int(v[0:2], 16)
        g = int(v[2:4], 16)
        b = int(v[4:6], 16)
        return RGBColor(r, g, b)
    except Exception:
        return None


def _pp_align(value: str) -> Optional[int]:
    v = (value or "").strip().lower()
    if not v:
        return None
    if v in {"left", "l"}:
        return PP_ALIGN.LEFT
    if v in {"center", "c", "centre"}:
        return PP_ALIGN.CENTER
    if v in {"right", "r"}:
        return PP_ALIGN.RIGHT
    if v in {"justify", "justified"}:
        return PP_ALIGN.JUSTIFY
    return None


def parse_slides(md: str) -> list[SlideBlock]:
    matches = list(_SLIDE_HEADER_RE.finditer(md))
    slides: list[SlideBlock] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        slides.append(SlideBlock(index=int(m.group(1)), title=m.group(2).strip(), block=md[start:end].strip()))
    return slides


def extract_elements_json(block: str) -> dict[str, Any]:
    m = _JSON_FENCE_RE.search(block)
    if not m:
        raise ValueError("missing ```json element inventory code fence")
    try:
        return json.loads(m.group(1))
    except Exception as e:
        raise ValueError(f"invalid JSON inventory: {e}") from e


def _bbox_pct_to_inches(bbox_pct: list[float], slide_w_in: float, slide_h_in: float) -> tuple[float, float, float, float]:
    if len(bbox_pct) != 4:
        raise ValueError("bbox_pct must have 4 numbers: [x,y,w,h]")
    x, y, w, h = bbox_pct
    return (
        slide_w_in * float(x) / 100.0,
        slide_h_in * float(y) / 100.0,
        slide_w_in * float(w) / 100.0,
        slide_h_in * float(h) / 100.0,
    )


def _add_textbox(slide, *, x: float, y: float, w: float, h: float, text: str, style: dict[str, Any]) -> None:
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear()

    lines = (text or "").splitlines() or [""]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        align = _pp_align(str(style.get("align", "")))
        if align is not None:
            p.alignment = align

        run = p.runs[0] if p.runs else p.add_run()
        run.text = line
        font = run.font
        if "font_size" in style:
            try:
                font.size = Pt(float(style["font_size"]))
            except Exception:
                pass
        if "bold" in style:
            font.bold = bool(style["bold"])
        if "italic" in style:
            font.italic = bool(style["italic"])
        if "font" in style:
            font.name = str(style["font"])
        color = _hex_to_rgb(str(style.get("color", "")))
        if color is not None:
            font.color.rgb = color


def _add_bullets(slide, *, x: float, y: float, w: float, h: float, items: list[str], style: dict[str, Any]) -> None:
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear()

    for i, item in enumerate(items or []):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = str(item)
        p.level = 0
        p.text = str(item)
        p.font.size = Pt(float(style.get("font_size", 18)))
        align = _pp_align(str(style.get("align", "")))
        if align is not None:
            p.alignment = align
        color = _hex_to_rgb(str(style.get("color", "")))
        if color is not None:
            p.font.color.rgb = color


def build_pptx(*, prompts_path: Path, output_path: Path, background_images_dir: Optional[Path]) -> None:
    md = prompts_path.read_text(encoding="utf-8")
    slides = parse_slides(md)
    if not slides:
        raise ValueError("no slides found (expected '## Slide N: ...' headers)")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_w_in = prs.slide_width.inches  # type: ignore[attr-defined]
    slide_h_in = prs.slide_height.inches  # type: ignore[attr-defined]
    blank = prs.slide_layouts[6]

    # Validate uniqueness and order.
    seen: set[int] = set()
    for s in slides:
        if s.index in seen:
            raise ValueError(f"duplicate slide number: {s.index}")
        seen.add(s.index)
    slides = sorted(slides, key=lambda s: s.index)

    for s in slides:
        slide = prs.slides.add_slide(blank)

        if background_images_dir is not None:
            # Best-effort match: 02_title.png naming (same as styled-artifacts).
            candidates = sorted(background_images_dir.glob(f"{s.index:02d}_*.png"))
            if candidates:
                slide.shapes.add_picture(str(candidates[0]), 0, 0, width=prs.slide_width, height=prs.slide_height)

        inventory = extract_elements_json(s.block)
        elements = inventory.get("elements")
        if not isinstance(elements, list) or not elements:
            raise ValueError(f"slide {s.index}: inventory missing 'elements' list")

        for el in elements:
            if not isinstance(el, dict):
                continue
            el_type = str(el.get("type", "")).strip().lower()
            bbox = el.get("bbox_pct")
            if not isinstance(bbox, list):
                continue
            x, y, w, h = _bbox_pct_to_inches([float(v) for v in bbox], slide_w_in, slide_h_in)
            style = el.get("style") if isinstance(el.get("style"), dict) else {}

            if el_type in {"title", "text"}:
                _add_textbox(slide, x=x, y=y, w=w, h=h, text=str(el.get("text", "")), style=style)
            elif el_type in {"bullets", "bullet_list", "list"}:
                items = el.get("items")
                if isinstance(items, list):
                    _add_bullets(slide, x=x, y=y, w=w, h=h, items=[str(i) for i in items], style=style)
            elif el_type == "code":
                s2 = dict(style)
                s2.setdefault("font", "Courier New")
                s2.setdefault("font_size", 16)
                _add_textbox(slide, x=x, y=y, w=w, h=h, text=str(el.get("text", "")), style=s2)
            elif el_type == "table":
                data = el.get("data")
                if isinstance(data, list) and data and all(isinstance(r, list) for r in data):
                    rows = len(data)
                    cols = max(len(r) for r in data)
                    tbl_shape = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
                    tbl = tbl_shape.table
                    for r in range(rows):
                        for c in range(cols):
                            val = ""
                            if c < len(data[r]):
                                val = str(data[r][c])
                            cell = tbl.cell(r, c)
                            cell.text = val
            else:
                # Skip unsupported elements in editable mode.
                # Diagrams/illustrations/icons are expected to be handled as images (or in image-PPTX mode).
                continue

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output_path))


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Generate an editable PPTX from v2 styled prompts (requires JSON element inventories)")
    p.add_argument("--prompts", required=True, help="Path to prompts/styled/*.md")
    p.add_argument("--out", required=True, help="Output PPTX path")
    p.add_argument("--background-images-dir", help="Optional directory of slide PNGs to place as a background layer")
    args = p.parse_args(argv)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"Prompts file not found: {prompts_path}", file=sys.stderr)
        return 2

    bg = Path(args.background_images_dir) if args.background_images_dir else None
    if bg is not None and not bg.exists():
        print(f"Background images dir not found: {bg}", file=sys.stderr)
        return 2

    try:
        build_pptx(prompts_path=prompts_path, output_path=Path(args.out), background_images_dir=bg)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

