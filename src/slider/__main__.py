from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .prompts import render_deck_prompts
from .spec import parse_markdown_spec
from .styles import get_style, list_style_names


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
