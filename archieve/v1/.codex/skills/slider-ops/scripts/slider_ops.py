from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


def _load_toml(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import tomllib  # type: ignore[attr-defined]

        data = tomllib.loads(text)
    except ModuleNotFoundError:
        import tomli  # type: ignore[import-not-found]

        data = tomli.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected TOML root table in {path}")
    return data


def _toml_multiline(value: str) -> str:
    if '"""' in value:
        raise ValueError('TOML multiline strings cannot contain """')
    value = value.rstrip() + "\n"
    return '"""\n' + value + '"""'


def _dump_style_file(general: Mapping[str, Any], layouts: Mapping[str, Mapping[str, Any]]) -> str:
    out: list[str] = []

    out.append("[GENERAL]")
    default_layout = str(general.get("default_layout", "") or "")
    if default_layout:
        out.append(f'default_layout = "{default_layout}"')
    out.append(f'style_prompt = {_toml_multiline(str(general.get("style_prompt", "") or ""))}')
    out.append("")

    for layout_name in sorted(layouts.keys(), key=str):
        table = layouts[layout_name]
        out.append(f"[layouts.{layout_name}]")
        out.append(f'layout_description = {_toml_multiline(str(table.get("layout_description", "") or ""))}')
        out.append(f'style_prompt = {_toml_multiline(str(table.get("style_prompt", "") or ""))}')
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _read_text_arg(repo_root: Path, value: str) -> str:
    if value == "-":
        return sys.stdin.read()
    if value.startswith("@"):
        p = Path(value[1:])
        if not p.is_absolute():
            p = repo_root / p
        return p.read_text(encoding="utf-8")
    return value


_STYLE_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_LAYOUT_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_]*$")


def _validate_style_name(name: str) -> str:
    if not _STYLE_NAME_RE.match(name):
        raise ValueError("Style name must match ^[a-z0-9][a-z0-9-]*$")
    return name


def _validate_layout_name(name: str) -> str:
    if not _LAYOUT_NAME_RE.match(name):
        raise ValueError("Layout name must match ^[a-z0-9][a-z0-9_]*$ (use underscores, not hyphens)")
    return name


def _find_repo_root(start: Path) -> Path:
    for candidate in [start] + list(start.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "src" / "slider").exists():
            return candidate
    raise RuntimeError("Could not locate repo root (expected pyproject.toml and src/slider)")


def _ensure_imports(repo_root: Path) -> None:
    sys.path.insert(0, str(repo_root / "src"))


def _resolve_repo_path(repo_root: Path, value: str | Path) -> Path:
    path = value if isinstance(value, Path) else Path(value)
    if path.is_absolute():
        return path
    return repo_root / path


def _styles_dir(repo_root: Path, styles_dir_arg: str) -> Path:
    return _resolve_repo_path(repo_root, styles_dir_arg)


def _style_file(repo_root: Path, styles_dir_arg: str, style: str) -> Path:
    return _styles_dir(repo_root, styles_dir_arg) / f"{style}.toml"


def cmd_styles_list(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    styles_dir = _styles_dir(repo_root, args.styles_dir)
    if not styles_dir.exists():
        return 0
    for p in sorted(styles_dir.glob("*.toml")):
        if p.is_file():
            print(p.stem)
    return 0


def cmd_styles_show(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    _ensure_imports(repo_root)
    from slider.styles import get_style

    style = get_style(args.style, _styles_dir(repo_root, args.styles_dir))
    print(f"Style: {style.name}")
    if style.default_layout:
        print(f"Default layout: {style.default_layout}")
    print("")
    print("General prompt:")
    print(style.general_style_prompt or "(empty)")
    print("")
    print("Layouts:")
    for name in style.available_layouts():
        layout = style.layouts[name]
        desc = layout.layout_description.strip() or "(empty)"
        print(f"- {name}: {desc}")
    return 0


def _load_style_tables(style_path: Path) -> tuple[Dict[str, Any], Dict[str, Dict[str, Any]]]:
    data = _load_toml(style_path)
    general = data.get("GENERAL", {}) or {}
    layouts = data.get("layouts", {}) or {}
    if not isinstance(general, dict):
        raise ValueError(f"TOML table [GENERAL] must be a table in {style_path}")
    if not isinstance(layouts, dict):
        raise ValueError(f"TOML table [layouts] must be a table in {style_path}")
    typed_layouts: Dict[str, Dict[str, Any]] = {}
    for name, table in layouts.items():
        if not isinstance(table, dict):
            raise ValueError(f"TOML table [layouts.{name}] must be a table in {style_path}")
        typed_layouts[str(name)] = dict(table)
    return dict(general), typed_layouts


def cmd_styles_create(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    styles_dir = _styles_dir(repo_root, args.styles_dir)
    styles_dir.mkdir(parents=True, exist_ok=True)

    style_name = _validate_style_name(args.style)
    target = _style_file(repo_root, args.styles_dir, style_name)
    if target.exists() and not args.force:
        raise FileExistsError(f"Style file already exists: {target} (use --force to overwrite)")

    general: Dict[str, Any] = {"style_prompt": ""}
    layouts: Dict[str, Dict[str, Any]] = {}

    if args.clone:
        clone_path = _style_file(repo_root, args.styles_dir, args.clone)
        if not clone_path.exists():
            raise FileNotFoundError(f"Clone style not found: {clone_path}")
        general, layouts = _load_style_tables(clone_path)

    if args.default_layout is not None:
        general["default_layout"] = args.default_layout

    if args.prompt is not None:
        general["style_prompt"] = _read_text_arg(repo_root, args.prompt)

    target.write_text(_dump_style_file(general=general, layouts=layouts), encoding="utf-8")
    print(str(target))
    return 0


def cmd_styles_delete(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    target = _style_file(repo_root, args.styles_dir, args.style)
    if not target.exists():
        raise FileNotFoundError(f"Style file not found: {target}")
    target.unlink()
    print(f"Deleted {target}")
    return 0


def cmd_styles_evolve(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    _ensure_imports(repo_root)

    from slider.style_evolve import evolve_style_file

    style_path = _style_file(repo_root, args.styles_dir, args.style)
    if not style_path.exists():
        raise FileNotFoundError(f"Style file not found: {style_path}")

    result = evolve_style_file(
        style_path=style_path,
        styles_dir=_styles_dir(repo_root, args.styles_dir),
        target=args.target,
        out_path=None,
        dry_run=bool(args.dry_run),
    )

    if args.dry_run:
        if result.added_layouts:
            for name in result.added_layouts:
                print(name)
        return 0

    print(str(result.out_path))
    return 0


def cmd_layouts_list(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    style_path = _style_file(repo_root, args.styles_dir, args.style)
    if not style_path.exists():
        raise FileNotFoundError(f"Style file not found: {style_path}")
    _, layouts = _load_style_tables(style_path)
    for name in sorted(layouts.keys()):
        print(name)
    return 0


def _parse_clone_ref(value: str, default_style: str) -> tuple[str, str]:
    if ":" in value:
        s, l = value.split(":", 1)
        return s.strip(), l.strip()
    return default_style, value.strip()


def cmd_layouts_upsert(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    style_name = _validate_style_name(args.style)
    layout_name = _validate_layout_name(args.layout)
    style_path = _style_file(repo_root, args.styles_dir, style_name)
    if not style_path.exists():
        raise FileNotFoundError(f"Style file not found: {style_path}")

    general, layouts = _load_style_tables(style_path)

    base: Dict[str, Any] = {}
    if args.clone:
        clone_style, clone_layout = _parse_clone_ref(args.clone, style_name)
        clone_style_path = _style_file(repo_root, args.styles_dir, clone_style)
        if not clone_style_path.exists():
            raise FileNotFoundError(f"Clone style not found: {clone_style_path}")
        _, clone_layouts = _load_style_tables(clone_style_path)
        if clone_layout not in clone_layouts:
            raise KeyError(f"Clone layout not found: {clone_layout} (in {clone_style_path})")
        base = dict(clone_layouts[clone_layout])
    elif layout_name in layouts:
        base = dict(layouts[layout_name])

    desc = (
        _read_text_arg(repo_root, args.description)
        if args.description is not None
        else str(base.get("layout_description", "") or "")
    )
    prompt = (
        _read_text_arg(repo_root, args.prompt) if args.prompt is not None else str(base.get("style_prompt", "") or "")
    )
    layouts[layout_name] = {"layout_description": desc, "style_prompt": prompt}

    style_path.write_text(_dump_style_file(general=general, layouts=layouts), encoding="utf-8")
    print(f"Upserted layout '{layout_name}' in {style_path}")
    return 0


def cmd_layouts_delete(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    style_path = _style_file(repo_root, args.styles_dir, args.style)
    if not style_path.exists():
        raise FileNotFoundError(f"Style file not found: {style_path}")
    general, layouts = _load_style_tables(style_path)
    if args.layout not in layouts:
        raise KeyError(f"Layout not found: {args.layout}")
    del layouts[args.layout]
    style_path.write_text(_dump_style_file(general=general, layouts=layouts), encoding="utf-8")
    print(f"Deleted layout '{args.layout}' from {style_path}")
    return 0


def cmd_prompts_render(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    _ensure_imports(repo_root)
    from slider.prompts import render_deck_prompts
    from slider.spec import parse_markdown_spec
    from slider.styles import get_style

    spec_path = _resolve_repo_path(repo_root, args.spec)
    deck = parse_markdown_spec(spec_path.read_text(encoding="utf-8"))
    style = get_style(args.style, _styles_dir(repo_root, args.styles_dir))
    rendered = render_deck_prompts(
        deck=deck,
        style=style,
        workflow_prompt_path=_resolve_repo_path(repo_root, args.workflow),
    )

    out_path = _resolve_repo_path(repo_root, args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    print(str(out_path))
    return 0


def cmd_spec_init(args: argparse.Namespace) -> int:
    repo_root = _find_repo_root(Path(__file__).resolve())
    out_path = _resolve_repo_path(repo_root, args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    slides = [s.strip() for s in (args.slides or "").split(",") if s.strip()]

    lines: list[str] = [f"# {args.title}".rstrip(), ""]
    if slides:
        for title in slides:
            lines.extend([f"## {title}", "", "- TODO", ""])
    else:
        lines.extend(["## Slide 1", "", "- TODO", ""])

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(str(out_path))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="slider_ops", description="Repo-local automation for slider")
    parser.add_argument("--styles-dir", default="styles", help="Directory containing style TOMLs")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_styles = sub.add_parser("styles", help="Style file operations")
    sub_styles = p_styles.add_subparsers(dest="styles_cmd", required=True)

    p_list = sub_styles.add_parser("list", help="List styles")
    p_list.set_defaults(func=cmd_styles_list)

    p_show = sub_styles.add_parser("show", help="Show a style summary")
    p_show.add_argument("style", help="Style name (filename stem)")
    p_show.set_defaults(func=cmd_styles_show)

    p_create = sub_styles.add_parser("create", help="Create a new style file (optionally cloning another)")
    p_create.add_argument("style", help="New style name (lowercase, digits, hyphens)")
    p_create.add_argument("--clone", help="Clone from an existing style name")
    p_create.add_argument("--default-layout", help="Set [GENERAL].default_layout")
    p_create.add_argument("--prompt", help="Set [GENERAL].style_prompt (literal, @file, or '-' for stdin)")
    p_create.add_argument("--force", action="store_true", help="Overwrite if the style file exists")
    p_create.set_defaults(func=cmd_styles_create)

    p_delete = sub_styles.add_parser("delete", help="Delete a style file")
    p_delete.add_argument("style", help="Style name")
    p_delete.set_defaults(func=cmd_styles_delete)

    p_evolve = sub_styles.add_parser("evolve", help="Add missing layouts to a style (canonical or union)")
    p_evolve.add_argument("style", help="Style name")
    p_evolve.add_argument(
        "--target",
        default="canonical",
        choices=["canonical", "all"],
        help="Which layouts to ensure exist (default: canonical)",
    )
    p_evolve.add_argument("--dry-run", action="store_true", help="Print missing layout names, do not write")
    p_evolve.set_defaults(func=cmd_styles_evolve)

    p_layouts = sub.add_parser("layouts", help="Layout operations inside a style file")
    sub_layouts = p_layouts.add_subparsers(dest="layouts_cmd", required=True)

    p_l_list = sub_layouts.add_parser("list", help="List layouts in a style")
    p_l_list.add_argument("style", help="Style name")
    p_l_list.set_defaults(func=cmd_layouts_list)

    p_l_upsert = sub_layouts.add_parser("upsert", help="Create/update a layout in a style (rewrites style file)")
    p_l_upsert.add_argument("style", help="Style name")
    p_l_upsert.add_argument("layout", help="Layout name (use underscores)")
    p_l_upsert.add_argument("--clone", help="Clone from '<layout>' or '<style>:<layout>'")
    p_l_upsert.add_argument("--description", help="layout_description (literal, @file, or '-' for stdin)")
    p_l_upsert.add_argument("--prompt", help="style_prompt (literal, @file, or '-' for stdin)")
    p_l_upsert.set_defaults(func=cmd_layouts_upsert)

    p_l_delete = sub_layouts.add_parser("delete", help="Delete a layout from a style")
    p_l_delete.add_argument("style", help="Style name")
    p_l_delete.add_argument("layout", help="Layout name")
    p_l_delete.set_defaults(func=cmd_layouts_delete)

    p_prompts = sub.add_parser("prompts", help="Prompt operations")
    sub_prompts = p_prompts.add_subparsers(dest="prompts_cmd", required=True)

    p_render = sub_prompts.add_parser("render", help="Render per-slide prompts from a spec")
    p_render.add_argument("--spec", required=True, help="Path to Markdown spec")
    p_render.add_argument("--style", required=True, help="Style name (filename stem)")
    p_render.add_argument("--workflow", default="prompts/workflow-prompt.md", help="Workflow prompt template path")
    p_render.add_argument("--out", required=True, help="Output path")
    p_render.set_defaults(func=cmd_prompts_render)

    p_spec = sub.add_parser("spec", help="Spec operations")
    sub_spec = p_spec.add_subparsers(dest="spec_cmd", required=True)

    p_init = sub_spec.add_parser("init", help="Create a starter Markdown spec")
    p_init.add_argument("--out", required=True, help="Output spec path")
    p_init.add_argument("--title", required=True, help="Deck title")
    p_init.add_argument("--slides", help="Comma-separated slide titles")
    p_init.set_defaults(func=cmd_spec_init)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
