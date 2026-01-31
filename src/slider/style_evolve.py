from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional

from .layout_catalog import CANONICAL_LAYOUTS, LayoutCatalogEntry


def _load_toml(path: Path) -> Mapping[str, Any]:
    data: Any
    try:
        import tomllib  # type: ignore[attr-defined]

        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except ModuleNotFoundError:
        import tomli  # type: ignore[import-not-found]

        data = tomli.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected TOML root table in {path}")
    return data


def _toml_multiline(value: str) -> str:
    if '"""' in value:
        raise ValueError('TOML multiline strings cannot contain """')
    value = value.rstrip() + "\n"
    return '"""\n' + value + '"""'


def _dump_layout_table(entry: LayoutCatalogEntry) -> str:
    lines: list[str] = []
    lines.append(f"[layouts.{entry.name}]")
    lines.append(f"layout_description = {_toml_multiline(entry.layout_description)}")
    lines.append(f"style_prompt = {_toml_multiline(entry.style_prompt)}")
    return "\n".join(lines).rstrip() + "\n"


def list_layout_names_in_style(style_path: Path) -> set[str]:
    data = _load_toml(style_path)
    layouts = data.get("layouts", {}) or {}
    if not isinstance(layouts, dict):
        raise ValueError(f"TOML table [layouts] must be a table in {style_path}")
    return {str(k) for k in layouts.keys()}


def union_layout_names_in_styles(styles_dir: Path, *, exclude: Optional[Iterable[Path]] = None) -> set[str]:
    excluded = {p.resolve() for p in (exclude or [])}
    names: set[str] = set()
    for p in sorted(styles_dir.glob("*.toml")):
        if not p.is_file():
            continue
        if p.resolve() in excluded:
            continue
        try:
            names |= list_layout_names_in_style(p)
        except Exception:
            # Best-effort: a single broken style file should not prevent evolution.
            continue
    return names


def _best_effort_description_from_other_styles(styles_dir: Path, layout_name: str, *, exclude: Path) -> str:
    excluded = exclude.resolve()
    for p in sorted(styles_dir.glob("*.toml")):
        if not p.is_file():
            continue
        if p.resolve() == excluded:
            continue
        try:
            data = _load_toml(p)
        except Exception:
            continue
        layouts = data.get("layouts", {}) or {}
        if not isinstance(layouts, dict):
            continue
        table = layouts.get(layout_name)
        if isinstance(table, dict):
            desc = str(table.get("layout_description", "") or "").strip()
            if desc:
                return desc
    return ""


def _generic_style_prompt(layout_name: str, layout_description: str) -> str:
    desc = layout_description.strip()
    header = f"Layout: {layout_name}"
    if desc:
        header += f" — {desc}"
    return (
        "Follow the [GENERAL].style_prompt global constraints.\n"
        "Keep the overall aesthetic consistent with other layouts already defined in this style.\n"
        "\n"
        f"{header}\n"
        "\n"
        "Structure:\n"
        "- Implement the layout described in layout_description.\n"
        "- Use clear hierarchy, consistent margins, and readable text.\n"
    )


@dataclass(frozen=True)
class StyleEvolutionResult:
    style_path: Path
    out_path: Path
    target: str
    added_layouts: tuple[str, ...]


def evolve_style_file(
    *,
    style_path: Path,
    styles_dir: Optional[Path] = None,
    target: str = "canonical",
    out_path: Optional[Path] = None,
    dry_run: bool = False,
) -> StyleEvolutionResult:
    """
    Add missing layout tables to a style TOML file.

    - target="canonical": ensure layouts used by infer_layout exist.
    - target="all": ensure union of layout names across styles_dir exists.
    """

    style_path = style_path.resolve()
    if styles_dir is None:
        styles_dir = style_path.parent
    styles_dir = styles_dir.resolve()

    if out_path is None:
        out_path = style_path
    out_path = out_path.resolve()

    existing = list_layout_names_in_style(style_path)

    target_names: set[str]
    if target == "canonical":
        target_names = set(CANONICAL_LAYOUTS.keys())
    elif target == "all":
        target_names = set(CANONICAL_LAYOUTS.keys()) | union_layout_names_in_styles(styles_dir, exclude=[style_path])
    else:
        raise ValueError("target must be 'canonical' or 'all'")

    missing = sorted([name for name in target_names if name not in existing])
    if dry_run:
        return StyleEvolutionResult(
            style_path=style_path,
            out_path=out_path,
            target=target,
            added_layouts=tuple(missing),
        )

    if not missing:
        if out_path != style_path:
            out_path.write_text(style_path.read_text(encoding="utf-8"), encoding="utf-8")
        return StyleEvolutionResult(
            style_path=style_path,
            out_path=out_path,
            target=target,
            added_layouts=tuple(),
        )

    additions: list[str] = []
    for name in missing:
        if name in CANONICAL_LAYOUTS:
            entry = CANONICAL_LAYOUTS[name]
            additions.append(_dump_layout_table(entry))
            continue

        desc = _best_effort_description_from_other_styles(styles_dir, name, exclude=style_path)
        entry = LayoutCatalogEntry(
            name=name,
            layout_description=desc,
            style_prompt=_generic_style_prompt(name, desc),
        )
        additions.append(_dump_layout_table(entry))

    original = style_path.read_text(encoding="utf-8")
    suffix = "\n".join([a.rstrip() for a in additions]).rstrip() + "\n"

    updated = original.rstrip() + "\n\n" + suffix.rstrip() + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(updated, encoding="utf-8")

    return StyleEvolutionResult(
        style_path=style_path,
        out_path=out_path,
        target=target,
        added_layouts=tuple(missing),
    )
