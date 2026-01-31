from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .prompts import render_deck_prompts
from .spec import parse_markdown_spec
from .spec_structurer import structure_material_to_spec_markdown
from .styles import get_style, list_style_names
from .style_evolve import evolve_style_file


def _cmd_list_styles(args: argparse.Namespace) -> int:
    for name in list_style_names(args.styles_dir):
        print(name)
    return 0


def _cmd_render_prompts(args: argparse.Namespace) -> int:
    spec_path = Path(args.spec)
    deck = parse_markdown_spec(spec_path.read_text(encoding="utf-8"))
    style = get_style(args.style, args.styles_dir)
    rendered = render_deck_prompts(deck=deck, style=style, workflow_prompt_path=args.workflow)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(str(out_path))
    return 0


def _cmd_structure_spec(args: argparse.Namespace) -> int:
    if args.material == "-":
        material_text = sys.stdin.read()
    else:
        material_text = Path(args.material).read_text(encoding="utf-8")

    spec_text = structure_material_to_spec_markdown(
        material_text,
        deck_title=args.title,
        max_bullets_per_slide=int(args.max_bullets),
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(spec_text, encoding="utf-8")
    print(str(out_path))
    return 0


def _cmd_evolve_style(args: argparse.Namespace) -> int:
    styles_dir = Path(args.styles_dir)
    if args.style_file:
        style_path = Path(args.style_file)
    else:
        style_path = styles_dir / f"{args.style}.toml"

    out_path = Path(args.out) if args.out else None
    result = evolve_style_file(
        style_path=style_path,
        styles_dir=styles_dir,
        target=args.target,
        out_path=out_path,
        dry_run=bool(args.dry_run),
    )

    if args.dry_run:
        if result.added_layouts:
            print("Missing layouts:")
            for name in result.added_layouts:
                print(f"- {name}")
        else:
            print("No missing layouts.")
        return 0

    print(str(result.out_path))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="slider", description="LLM slide prompt scaffolding")
    parser.set_defaults(func=None)

    parser.add_argument(
        "--styles-dir",
        default="styles",
        help="Directory containing style TOML files (default: styles/)",
    )

    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list-styles", help="List available styles")
    p_list.set_defaults(func=_cmd_list_styles)

    p_render = sub.add_parser("render-prompts", help="Render per-slide prompts from a Markdown SPEC")
    p_render.add_argument("--spec", required=True, help="Path to Markdown spec, e.g. specs/deck.md")
    p_render.add_argument("--style", required=True, help="Style name from styles TOML, e.g. minimal")
    p_render.add_argument(
        "--workflow",
        default="prompts/workflow-prompt.md",
        help="Path to workflow prompt template",
    )
    p_render.add_argument(
        "--out",
        required=True,
        help="Output path, e.g. prompts/generated/deck.md",
    )
    p_render.set_defaults(func=_cmd_render_prompts)

    p_structure = sub.add_parser(
        "structure-spec",
        help="Convert unstructured Markdown material into a structured SPEC (multi-slide Markdown)",
    )
    p_structure.add_argument(
        "--material",
        required=True,
        help="Path to unstructured Markdown material (or '-' for stdin)",
    )
    p_structure.add_argument(
        "--out",
        required=True,
        help="Output SPEC path, e.g. specs/mydeck.md",
    )
    p_structure.add_argument(
        "--title",
        help="Optional deck title override (defaults to first H1)",
    )
    p_structure.add_argument(
        "--max-bullets",
        default=6,
        type=int,
        help="Max bullets per slide before splitting into continuation slides (default: 6)",
    )
    p_structure.set_defaults(func=_cmd_structure_spec)

    p_evolve = sub.add_parser(
        "evolve-style",
        help="Add missing layouts to a style TOML (canonical or union across styles/)",
    )
    group = p_evolve.add_mutually_exclusive_group(required=True)
    group.add_argument("--style", help="Style name (filename stem), e.g. colorful-handdraw")
    group.add_argument("--style-file", help="Path to a style TOML file, e.g. styles/colorful-handdraw.toml")
    p_evolve.add_argument(
        "--target",
        default="canonical",
        choices=["canonical", "all"],
        help="Which layouts to ensure exist (default: canonical)",
    )
    p_evolve.add_argument(
        "--out",
        help="Optional output path (default: overwrite the input style file)",
    )
    p_evolve.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write; print missing layout names",
    )
    p_evolve.set_defaults(func=_cmd_evolve_style)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.func is None:
        parser.print_help()
        return 2
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
