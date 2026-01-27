# Styles

Styles are stored as one TOML file per style in `styles/` (e.g. `styles/minimal.toml`).

- `[GENERAL]` defines style-wide settings:
  - `default_layout` (optional): fallback layout name
  - `style_prompt`: style-wide visual guidance
- `[layouts.<layout-name>]` defines one layout entry:
  - `layout_description`: how the layout behaves
  - `style_prompt`: layout-specific styling/constraints
