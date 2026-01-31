#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


_SLIDE_HEADER_RE = re.compile(r"^##\s+Slide\s+(\d+):\s+(.+?)\s*$", re.M)


@dataclass(frozen=True)
class ParsedSlide:
    index: int
    title: str
    layout: str
    layout_description: str
    layout_prompt: str
    bullets: list[str]
    body: list[str]
    images: list[tuple[str, str]]  # (alt, src)


def _find_repo_root(start: Path) -> Path:
    for candidate in [start] + list(start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "src" / "slider").exists():
            return candidate
    return start.resolve()


def _slug(text: str, max_len: int = 48) -> str:
    t = text.strip().lower()
    t = re.sub(r"[^a-z0-9]+", "_", t).strip("_")
    if not t:
        return "slide"
    return t[:max_len].rstrip("_")


def _extract_section(text: str, start_marker: str) -> str:
    idx = text.find(start_marker)
    if idx < 0:
        return ""
    rest = text[idx + len(start_marker) :]
    if rest.startswith("\n"):
        rest = rest[1:]
    # Stop at next markdown heading of the same level or above.
    for m in re.finditer(r"^##\s+", rest, re.M):
        return rest[: m.start()].strip()
    return rest.strip()


def _extract_list(text: str, start_marker: str) -> list[str]:
    section = _extract_section(text, start_marker)
    if not section:
        return []
    out: list[str] = []
    for line in section.splitlines():
        m = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if m:
            out.append(m.group(1).strip())
        elif line.strip():
            out.append(line.strip())
    return [x for x in out if x]


def _parse_slide_block(index: int, title: str, block: str) -> ParsedSlide:
    layout = ""
    for line in block.splitlines():
        if line.startswith("Layout:"):
            layout = line[len("Layout:") :].strip()
            if "(" in layout:
                layout = layout.split("(", 1)[0].strip()
            break

    layout_description = _extract_section(block, "Layout description:")
    layout_prompt = _extract_section(block, "Layout prompt:")
    bullets = _extract_list(block, "Content (bullets):")
    body = _extract_list(block, "Content (body):")

    images: list[tuple[str, str]] = []
    images_section = _extract_section(block, "Images:")
    if images_section:
        for line in images_section.splitlines():
            # "- alt: ... | src: ..."
            m = re.match(r"^\s*-\s+alt:\s*(.*?)\s*\|\s*src:\s*(.+?)\s*$", line)
            if m:
                images.append((m.group(1).strip(), m.group(2).strip()))
    return ParsedSlide(
        index=index,
        title=title.strip(),
        layout=layout,
        layout_description=layout_description,
        layout_prompt=layout_prompt,
        bullets=bullets,
        body=body,
        images=images,
    )


def parse_slider_generated_prompts(text: str) -> tuple[str, list[ParsedSlide]]:
    """
    Parse slider's prompts/generated/*.md format (rendered by slider.render_deck_prompts).
    Returns (general_style_prompt, slides).
    """
    general_style_prompt = _extract_section(text, "## Style: general prompt")

    matches = list(_SLIDE_HEADER_RE.finditer(text))
    slides: list[ParsedSlide] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        idx = int(m.group(1))
        title = m.group(2)
        block = text[start:end].strip()
        slides.append(_parse_slide_block(idx, title, block))
    return general_style_prompt, slides


def _is_http_url(value: str) -> bool:
    try:
        u = urllib.parse.urlparse(value)
        return u.scheme in {"http", "https"} and bool(u.netloc)
    except Exception:
        return False


def _download_url(url: str, dest_dir: Path) -> Optional[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    parsed = urllib.parse.urlparse(url)
    name = Path(parsed.path).name or "image"
    # Remove querystring-derived filename surprises.
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    if "." not in name:
        name += ".bin"
    out = dest_dir / name
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            out.write_bytes(resp.read())
        return out
    except Exception:
        return None


def _resolve_attachment(repo_root: Path, prompts_path: Path, src: str, downloads_dir: Path) -> Optional[Path]:
    src = src.strip()
    if not src:
        return None
    p = Path(src)
    if p.is_absolute() and p.exists():
        return p
    # Try relative to repo root and prompts file.
    candidates = [
        repo_root / src,
        prompts_path.parent / src,
        prompts_path.parent.parent / src,
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            return c
    if _is_http_url(src):
        return _download_url(src, downloads_dir)
    return None


def _build_slide_prompt(slide: ParsedSlide, general_style_prompt: str) -> str:
    parts: list[str] = []
    parts.append("Create a single presentation slide as a high-resolution 16:9 image.")
    parts.append(f"Slide title: {slide.title}")
    if slide.layout:
        parts.append(f"Layout: {slide.layout}")

    if general_style_prompt.strip():
        parts.append("")
        parts.append("Global style constraints (follow strictly):")
        parts.append(general_style_prompt.strip())

    if slide.layout_prompt.strip():
        parts.append("")
        parts.append("Layout-specific prompt (follow strictly):")
        parts.append(slide.layout_prompt.strip())

    if slide.layout_description.strip():
        parts.append("")
        parts.append("Layout behavior description (implement):")
        parts.append(slide.layout_description.strip())

    if slide.bullets:
        parts.append("")
        parts.append("Slide content (bullets):")
        parts.extend([f"- {b}" for b in slide.bullets])

    if slide.body:
        parts.append("")
        parts.append("Slide content (body lines):")
        parts.extend([f"- {b}" for b in slide.body])

    parts.append("")
    parts.append("Constraints:")
    parts.append("- Keep text minimal and readable; do not create dense paragraphs.")
    parts.append("- Do not invent data or citations.")
    parts.append("- Keep the visual language consistent across slides.")
    parts.append("FORMATTING GOAL: Match attached slide style exactly.")
    return "\n".join(parts).strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate slide images + PDF/PPTX from slider-generated prompts",
    )
    parser.add_argument("--prompts", required=True, help="Path to prompts/generated/<deck>.md")
    parser.add_argument("--out-dir", required=True, help="Output directory (e.g., artifacts/mydeck)")
    parser.add_argument("--pdf", help="Optional PDF output path")
    parser.add_argument("--pptx", help="Optional PPTX output path")
    parser.add_argument("--visual-only", action="store_true", help="Generate visuals only (not full slides)")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY env var)")
    parser.add_argument("--no-download", action="store_true", help="Do not download http(s) image URLs")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    prompts_path = Path(args.prompts).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_slides_dir = out_dir / "slides"
    out_slides_dir.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(Path.cwd().resolve())
    file_key_path = repo_root / ".OPENROUTER_API_KEY"
    file_key = ""
    if file_key_path.exists():
        try:
            file_key = file_key_path.read_text(encoding="utf-8").strip()
        except Exception:
            file_key = ""

    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY") or file_key
    if not api_key:
        print("Error: OPENROUTER_API_KEY not set (env var, --api-key, or .OPENROUTER_API_KEY file)")
        return 1

    text = prompts_path.read_text(encoding="utf-8")
    general_style_prompt, slides = parse_slider_generated_prompts(text)
    if not slides:
        raise SystemExit(f"No slides found in {prompts_path}")

    script_dir = Path(__file__).resolve().parent
    gen_script = script_dir / "generate_slide_image.py"
    if not gen_script.exists():
        raise SystemExit(f"Missing generator script: {gen_script}")

    downloads_dir = out_dir / "_downloads"

    previous_slide: Optional[Path] = None
    for slide in slides:
        prompt = _build_slide_prompt(slide, general_style_prompt)
        filename = f"{slide.index:02d}_{_slug(slide.title)}.png"
        out_img = out_slides_dir / filename

        cmd: list[str] = [sys.executable, str(gen_script), prompt, "-o", str(out_img)]

        if args.visual_only:
            cmd.append("--visual-only")

        cmd.extend(["--api-key", api_key])

        attachments: list[Path] = []
        if previous_slide and previous_slide.exists():
            attachments.append(previous_slide)

        for _, src in slide.images:
            if _is_http_url(src) and args.no_download:
                continue
            att = _resolve_attachment(repo_root, prompts_path, src, downloads_dir)
            if att:
                attachments.append(att)

        for att in attachments:
            cmd.extend(["--attach", str(att)])

        if args.verbose:
            print(f"[slide {slide.index}] {out_img.name}")
            if attachments:
                print("  attachments:")
                for a in attachments:
                    print(f"  - {a}")

        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            return int(result.returncode)

        previous_slide = out_img

    if args.pdf:
        pdf_script = script_dir / "slides_to_pdf.py"
        cmd = [sys.executable, str(pdf_script), str(out_slides_dir), "-o", str(Path(args.pdf).resolve())]
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            return int(result.returncode)

    if args.pptx:
        pptx_script = script_dir / "slides_to_pptx.py"
        cmd = [sys.executable, str(pptx_script), str(out_slides_dir), "-o", str(Path(args.pptx).resolve())]
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            return int(result.returncode)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
