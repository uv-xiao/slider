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


def _parse_only(value: str) -> set[int]:
    """
    Parse a slide selection string like:
      - "3"
      - "2,5,8"
      - "5-8"
      - "1,3-5,9"
    """
    out: set[int] = set()
    for part in (value or "").split(","):
        p = part.strip()
        if not p:
            continue
        if "-" in p:
            a, b = p.split("-", 1)
            a_i = int(a.strip())
            b_i = int(b.strip())
            if a_i <= 0 or b_i <= 0:
                raise ValueError("slide numbers must be positive")
            lo, hi = (a_i, b_i) if a_i <= b_i else (b_i, a_i)
            out.update(range(lo, hi + 1))
        else:
            i = int(p)
            if i <= 0:
                raise ValueError("slide numbers must be positive")
            out.add(i)
    if not out:
        raise ValueError("empty slide selection")
    return out


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


def _pick_workdir(base: Path, *, reuse: bool) -> Path:
    """
    If `base` already exists and `reuse` is False, create a new version:
      base-2, base-3, ...
    """
    if reuse or not base.exists():
        return base

    for i in range(2, 10_000):
        candidate = base.with_name(f"{base.name}-{i}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find an available workdir version for: {base}")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Generate slide images + PDF/PPTX from v2 styled prompts")
    p.add_argument("--prompts", required=True, help="Path to prompts/styled/*.md")
    p.add_argument("--workdir", required=True, help="Work directory (slides written under workdir/slides/)")
    p.add_argument("--pdf", help="Optional PDF output path")
    p.add_argument("--pptx", help="Optional PPTX output path")
    p.add_argument("--pptx-editable", help="Optional editable PPTX output path (requires JSON element inventories in styled prompts)")
    p.add_argument(
        "--pptx-editable-with-background",
        action="store_true",
        help="For --pptx-editable: place generated slide PNGs as a background layer under editable elements",
    )
    p.add_argument(
        "--skip-slide-images",
        action="store_true",
        help="Skip slide PNG generation (useful for editable PPTX only). Incompatible with --pdf/--pptx/--pptx-editable-with-background.",
    )
    p.add_argument("--only", help="Only generate a subset of slides (e.g. '3' or '2,5,8' or '5-8')")
    p.add_argument("--reuse-workdir", action="store_true", help="Reuse workdir if it exists (default is to create workdir-N)")
    p.add_argument("--allow-empty-global-context", action="store_true", help="Allow styled prompts with no deck-level global context")
    p.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY / .OPENROUTER_API_KEY)")
    p.add_argument("--no-download", action="store_true", help="Disable downloading http(s) image URLs")
    args = p.parse_args(argv)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"Prompts file not found: {prompts_path}", file=sys.stderr)
        return 2

    base_workdir = Path(args.workdir)
    selected: Optional[set[int]] = None
    if args.only:
        try:
            selected = _parse_only(args.only)
        except Exception as e:
            print(f"Invalid --only value: {e}", file=sys.stderr)
            return 2

    # Default: avoid clobbering previous work. If the user is doing an incremental regeneration,
    # they'll typically want to reuse the same workdir.
    reuse_workdir = bool(args.reuse_workdir) or bool(selected)
    workdir = _pick_workdir(base_workdir, reuse=reuse_workdir)
    if workdir != base_workdir:
        print(f"Workdir exists; writing into: {workdir}")

    slides_dir = workdir / "slides"
    downloads_dir = workdir / "downloads"
    raster_dir = workdir / "rasterized"
    slides_dir.mkdir(parents=True, exist_ok=True)

    # Prefer resolving the repo root from this script's location so the tool
    # works even when --prompts points outside the repo (e.g. /tmp during tests).
    repo_root = _find_repo_root(Path(__file__).resolve().parent)

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
    if not global_context.strip() and not args.allow_empty_global_context:
        print(
            "Styled prompts are missing deck-level global context (text before the first '## Slide N:').\n"
            "Add a deck-level style/formatting contract at the top of the file, or rerun with --allow-empty-global-context.",
            file=sys.stderr,
        )
        return 2

    indices = [s.index for s in slides]
    seen: set[int] = set()
    duplicates: list[int] = []
    for i in indices:
        if i in seen:
            duplicates.append(i)
        seen.add(i)
    if duplicates:
        d = sorted(set(duplicates))
        print(f"Duplicate slide numbers found: {d}. Slide numbers must be unique.", file=sys.stderr)
        return 2

    slides = sorted(slides, key=lambda s: s.index)

    gen_script = Path(__file__).resolve().parent / "generate_slide_image_ai.py"
    if not gen_script.exists():
        print(f"Missing generator script: {gen_script}", file=sys.stderr)
        return 2

    previous_slide: Optional[Path] = None
    slide_images: list[Path] = []

    needs_slide_images = bool(args.pdf) or bool(args.pptx) or bool(args.pptx_editable_with_background) or not bool(args.skip_slide_images)
    if args.skip_slide_images and (args.pdf or args.pptx or args.pptx_editable_with_background):
        print(
            "--skip-slide-images is incompatible with --pdf/--pptx/--pptx-editable-with-background.",
            file=sys.stderr,
        )
        return 2

    if needs_slide_images:
        for slide in slides:
            if selected is not None and slide.index not in selected:
                continue
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

            cmd = [sys.executable, str(gen_script), prompt, "-o", str(out_path)]
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
                print("✗ Generation failed.", file=sys.stderr)
                return int(proc.returncode)

            slide_images.append(out_path)
            previous_slide = out_path

        if selected is None:
            print(f"Generated {len(slide_images)} slide image(s)")
        else:
            print(f"Generated {len(slide_images)} slide image(s) for --only={args.only}")

    requires_full_deck_images = bool(args.pdf) or bool(args.pptx) or bool(args.pptx_editable_with_background)
    if requires_full_deck_images and selected is not None:
        missing: list[int] = []
        for slide in slides:
            expected = slides_dir / f"{slide.index:02d}_{_slug(slide.title)}.png"
            if not expected.exists():
                missing.append(slide.index)
        if missing:
            print(
                "Cannot assemble full PDF/PPTX because some slide images are missing in the workdir.\n"
                f"Missing slide(s): {missing}\n"
                "Tip: rerun without --only, or rerun with --reuse-workdir and keep prior slides in the same workdir.",
                file=sys.stderr,
            )
            return 2

    if args.pdf:
        pdf_script = Path(__file__).resolve().parent / "slides_to_pdf.py"
        subprocess.run([sys.executable, str(pdf_script), str(slides_dir), "-o", str(Path(args.pdf))], check=True)

    if args.pptx:
        ppt_script = repo_root / ".codex" / "skills" / "pptx" / "scripts" / "images_to_pptx.py"
        if not ppt_script.exists():
            print(f"Missing PPTX builder from pptx skill: {ppt_script}", file=sys.stderr)
            return 2
        subprocess.run([sys.executable, str(ppt_script), str(slides_dir), "-o", str(Path(args.pptx))], check=True)

    if args.pptx_editable:
        editable_script = repo_root / ".codex" / "skills" / "pptx" / "scripts" / "styled_prompts_to_editable_pptx.py"
        if not editable_script.exists():
            print(f"Missing editable PPTX builder from pptx skill: {editable_script}", file=sys.stderr)
            return 2
        cmd = [sys.executable, str(editable_script), "--prompts", str(prompts_path), "--out", str(Path(args.pptx_editable))]
        if args.pptx_editable_with_background:
            cmd.extend(["--background-images-dir", str(slides_dir)])
        subprocess.run(cmd, check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
