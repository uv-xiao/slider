# Style schema (styles/*.toml)

Each style is stored in its own TOML file, e.g. `styles/minimal.toml`.

## Tables

- `[GENERAL]`
  - `style_prompt` (string): general visual guidance for the whole deck
  - `default_layout` (string, optional): fallback layout name if inference selects an unavailable layout
- `[layouts.<layout_name>]`
  - `layout_description` (string): how the layout behaves
  - `style_prompt` (string): layout-specific constraints/guidance

## Notes

- Style name is the filename stem (`minimal` -> `styles/minimal.toml`).
- Layout names should match what `slider.spec.infer_layout` emits (e.g. `title_bullets`, `two_column_bullets`).

