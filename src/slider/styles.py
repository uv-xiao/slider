from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


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


@dataclass(frozen=True)
class Layout:
    name: str
    layout_description: str
    style_prompt: str


@dataclass(frozen=True)
class Style:
    name: str
    general_style_prompt: str
    default_layout: Optional[str]
    layouts: Mapping[str, Layout]

    def available_layouts(self) -> list[str]:
        return sorted(self.layouts.keys())

    def get_layout(self, name: str) -> Layout:
        if name not in self.layouts:
            available = ", ".join(self.available_layouts())
            raise KeyError(f"Unknown layout '{name}'. Available: {available}")
        return self.layouts[name]


def list_style_names(styles_dir: str | Path = "styles") -> list[str]:
    directory = Path(styles_dir)
    if not directory.exists():
        return []
    return sorted([p.stem for p in directory.glob("*.toml") if p.is_file()])


def style_file_path(name: str, styles_dir: str | Path = "styles") -> Path:
    return Path(styles_dir) / f"{name}.toml"


def _load_style_file(style_file: Path) -> Style:
    data = _load_toml(style_file)
    general = data.get("GENERAL", {}) or {}
    layouts = data.get("layouts", {}) or {}
    if not isinstance(general, dict):
        raise ValueError(f"TOML table [GENERAL] must be a table in {style_file}")
    if not isinstance(layouts, dict):
        raise ValueError(f"TOML table [layouts] must be a table in {style_file}")

    parsed_layouts: Dict[str, Layout] = {}
    for layout_name, value in layouts.items():
        if not isinstance(value, dict):
            raise ValueError(f"TOML table [layouts.{layout_name}] must be a table in {style_file}")
        parsed_layouts[str(layout_name)] = Layout(
            name=str(layout_name),
            layout_description=str(value.get("layout_description", "") or ""),
            style_prompt=str(value.get("style_prompt", "") or ""),
        )

    default_layout_raw = general.get("default_layout")
    default_layout: Optional[str]
    if default_layout_raw is None or default_layout_raw == "":
        default_layout = None
    else:
        default_layout = str(default_layout_raw)

    return Style(
        name=style_file.stem,
        general_style_prompt=str(general.get("style_prompt", "") or ""),
        default_layout=default_layout,
        layouts=parsed_layouts,
    )


def get_style(name: str, styles_dir: str | Path = "styles") -> Style:
    style_file = style_file_path(name, styles_dir)
    if not style_file.exists():
        available = ", ".join(list_style_names(styles_dir))
        raise FileNotFoundError(f"Style '{name}' not found at {style_file}. Available: {available}")
    return _load_style_file(style_file)

