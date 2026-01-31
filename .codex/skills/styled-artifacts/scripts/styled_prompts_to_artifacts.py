#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


_SLIDE_HEADER_RE = re.compile(r"^##\s+Slide\s+(\d+):\s+(.+?)\s*$", re.M)
_MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_ALT_SRC_RE = re.compile(r"^\s*-\s+alt:\s*(.*?)\s*\|\s*src:\s*(.+?)\s*$")


@dataclass(frozen=True)
class ParsedSlide:
    index: int
    title: str
    block: str
    images: list[tuple[str, str]]  # (alt, src)


def _find_repo_root(start: Path) -> Path:
    for candidate in [start] + list(start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start.resolve()


def _slug(text: str, max_len: int = 48) -> str:
    t = text.strip().lower()
    t = re.sub(r"[^a-z0-9]+", "_", t).strip("_")
    return (t or "slide")[:max_len].rstrip("_")


def parse_styled_prompts(text: str) -> tuple[str, list[ParsedSlide]]:
    matches = list(_SLIDE_HEADER_RE.finditer(text))
    global_context = text[: matches[0].start()].strip() if matches else text.strip()

    slides: list[ParsedSlide] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        index = int(m.group(1))
        title = m.group(2).strip()
        block = text[start:end].strip()

        images: list[tuple[str, str]] = []
        for alt, src in _MD_IMAGE_RE.findall(block):
            images.append((alt.strip(), src.strip()))
        for line in block.splitlines():
            m2 = _ALT_SRC_RE.match(line)
            if m2:
                images.append((m2.group(1).strip(), m2.group(2).strip()))

        slides.append(ParsedSlide(index=index, title=title, block=block, images=images))
    return global_context, slides


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


def _resolve_attachment(repo_root: Path, prompts_path: Path, src: str, downloads_dir: Path, *, allow_download: bool) -> Optional[Path]:
    src = src.strip()
    if not src:
        return None
    p = Path(src)
    if p.is_absolute() and p.exists():
        return p

    candidates = [
        repo_root / src,
        prompts_path.parent / src,
        prompts_path.parent.parent / src,
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            return c

    if allow_download and _is_http_url(src):
        return _download_url(src, downloads_dir)
    return None


def _rasterize_svg(svg_path: Path, raster_dir: Path) -> Optional[Path]:
    raster_dir.mkdir(parents=True, exist_ok=True)
    out = raster_dir / f"{svg_path.stem}.png"
    convert = shutil.which("convert")
    if not convert:
        return None
    try:
        subprocess.run(
            [convert, str(svg_path), "-background", "white", "-alpha", "remove", "-alpha", "off", str(out)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return out if out.exists() else None
    except Exception:
        return None


def _normalize_attachment(path: Path, raster_dir: Path) -> Path:
    if path.suffix.lower() == ".svg":
        raster = _rasterize_svg(path, raster_dir)
        if raster:
            return raster
    return path


def _build_slide_prompt(slide: ParsedSlide, global_context: str) -> str:
    parts: list[str] = []
    parts.append("Create a single presentation slide as a high-resolution 16:9 image.")
    parts.append("Follow the slide specification exactly; do not omit any required element.")
    parts.append("If the spec provides bounding boxes/positions, treat them as the source of truth.")
    parts.append(f"Slide title: {slide.title}")

    if global_context.strip():
        parts.append("")
        parts.append("Global context (apply across all slides):")
        parts.append(global_context.strip())

    parts.append("")
    parts.append("Slide specification:")
    parts.append(slide.block.strip())

    return "\n".join(parts).strip() + "\n"


def _parse_int_set(value: str) -> set[int]:
    """
    Parse comma-separated ints and ranges like:
      "1,2,5-7"
    """
    out: set[int] = set()
    for part in [p.strip() for p in value.split(",") if p.strip()]:
        if "-" in part:
            a, b = [x.strip() for x in part.split("-", 1)]
            if not a or not b:
                continue
            start = int(a)
            end = int(b)
            lo, hi = (start, end) if start <= end else (end, start)
            for i in range(lo, hi + 1):
                out.add(int(i))
        else:
            out.add(int(part))
    return out


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Generate slide images + PDF/PPTX from v2 styled prompts")
    p.add_argument("--prompts", required=True, help="Path to prompts/styled/*.md")
    p.add_argument("--workdir", required=True, help="Work directory (slides written under workdir/slides/)")
    p.add_argument("--pdf", help="Optional PDF output path")
    p.add_argument("--pptx", help="Optional PPTX output path")
    p.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY / .OPENROUTER_API_KEY)")
    p.add_argument("--no-download", action="store_true", help="Disable downloading http(s) image URLs")
    p.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip slide image generation when output PNG already exists (use --regenerate to override).",
    )
    p.add_argument(
        "--only",
        help="Only generate these slide indices (e.g. '1,3,5-7'). Others are skipped if their PNG exists.",
    )
    p.add_argument(
        "--regenerate",
        help="Regenerate these slide indices even if PNG exists (e.g. '2,5' or '1-3').",
    )
    p.add_argument("--iterations", type=int, default=2, help="Max refinement iterations per slide (default: 2)")
    p.add_argument(
        "--quality-threshold",
        type=float,
        default=6.5,
        help="Quality threshold 0-10 (default: 6.5)",
    )
    args = p.parse_args(argv)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"Prompts file not found: {prompts_path}", file=sys.stderr)
        return 2

    workdir = Path(args.workdir)
    slides_dir = workdir / "slides"
    downloads_dir = workdir / "downloads"
    raster_dir = workdir / "rasterized"
    slides_dir.mkdir(parents=True, exist_ok=True)

    repo_root = _find_repo_root(prompts_path.parent)

    # Allow key stored in repo root for local runs.
    if not args.api_key:
        key_path = repo_root / ".OPENROUTER_API_KEY"
        if key_path.exists():
            try:
                key = key_path.read_text(encoding="utf-8").strip()
                if key:
                    args.api_key = key
            except Exception:
                pass

    global_context, slides = parse_styled_prompts(prompts_path.read_text(encoding="utf-8"))
    if not slides:
        print("No slides found in prompts file.", file=sys.stderr)
        return 2

    gen_script = Path(__file__).resolve().parent / "generate_slide_image_ai.py"
    if not gen_script.exists():
        print(f"Missing generator script: {gen_script}", file=sys.stderr)
        return 2

    only_indices = _parse_int_set(args.only) if args.only else None
    regenerate_indices = _parse_int_set(args.regenerate) if args.regenerate else set()

    previous_slide: Optional[Path] = None
    slide_images: list[Path] = []

    for slide in slides:
        prompt = _build_slide_prompt(slide, global_context)

        attachments: list[Path] = []
        if previous_slide and previous_slide.exists():
            attachments.append(previous_slide)

        for alt, src in slide.images:
            resolved = _resolve_attachment(
                repo_root,
                prompts_path,
                src,
                downloads_dir,
                allow_download=not args.no_download,
            )
            if resolved is None:
                print(f"Warning: could not resolve image '{src}' for slide {slide.index} ({alt})")
                continue
            attachments.append(_normalize_attachment(resolved, raster_dir=raster_dir))

        out_name = f"{slide.index:02d}_{_slug(slide.title)}.png"
        out_path = slides_dir / out_name

        if only_indices is not None and slide.index not in only_indices:
            if out_path.exists():
                previous_slide = out_path
                slide_images.append(out_path)
            continue

        should_generate = True
        if slide.index in regenerate_indices:
            should_generate = True
        elif args.skip_existing and out_path.exists():
            should_generate = False

        if should_generate:
            cmd = [sys.executable, str(gen_script), prompt, "-o", str(out_path)]
            cmd.extend(["--iterations", str(int(args.iterations))])
            cmd.extend(["--quality-threshold", str(float(args.quality_threshold))])
            if args.api_key:
                cmd.extend(["--api-key", args.api_key])
            for a in attachments:
                cmd.extend(["--attach", str(a)])

            print("\n" + "=" * 60)
            print("Generating Slide Image")
            print("=" * 60)
            print(f"Slide title: {slide.title}")
            if attachments:
                print(f"Attachments: {len(attachments)} file(s)")
                for a in attachments:
                    print(f"  - {a}")
            print(f"Output: {out_path}")
            print("=" * 60 + "\n")

            proc = subprocess.run(cmd)
            if proc.returncode != 0:
                print("✗ Generation failed. Check review log for details.", file=sys.stderr)
                return int(proc.returncode)

        slide_images.append(out_path)
        previous_slide = out_path

    print(f"Found {len(slide_images)} image(s)")

    if args.pdf:
        pdf_script = Path(__file__).resolve().parent / "slides_to_pdf.py"
        subprocess.run([sys.executable, str(pdf_script), str(slides_dir), "-o", str(Path(args.pdf))], check=True)

        validate = Path(__file__).resolve().parent / "validate_presentation.py"
        subprocess.run([sys.executable, str(validate), str(Path(args.pdf))], check=False)

    if args.pptx:
        ppt_script = Path(__file__).resolve().parent / "slides_to_pptx.py"
        subprocess.run([sys.executable, str(ppt_script), str(slides_dir), "-o", str(Path(args.pptx))], check=True)

        validate = Path(__file__).resolve().parent / "validate_presentation.py"
        subprocess.run([sys.executable, str(validate), str(Path(args.pptx))], check=False)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
