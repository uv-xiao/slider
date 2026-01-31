---
name: style-evolve
description: "Evolve a slider style TOML (styles/*.toml) to support missing layouts while keeping the overall style consistent. Use when asked to 'add missing layouts', 'ensure a style supports title_bullets/two_column_bullets/image_*', 'evolve styles/colorful-handdraw.toml to support other layouts', or 'make a style support all layouts from other styles'."
---

# Style Evolve

Add missing `[layouts.*]` entries to a style TOML without overwriting any existing layouts. The new entries are written with layout-aware defaults that defer to `[GENERAL].style_prompt` so the look stays consistent.

## Quick start

- Evolve a style in-place (canonical layouts used by `infer_layout`):
  - `python3 -m slider evolve-style --style colorful-handdraw --target canonical`

- Evolve a style to include the union of layouts across `styles/*.toml`:
  - `python3 -m slider evolve-style --style colorful-handdraw --target all`

## Via slider-ops

- In-place evolve (canonical):
  - `python3 .codex/skills/slider-ops/scripts/slider_ops.py styles evolve colorful-handdraw --target canonical`

- Preview what would be added (no writes):
  - `python3 .codex/skills/slider-ops/scripts/slider_ops.py styles evolve colorful-handdraw --target canonical --dry-run`

## Notes / Guardrails

- This operation only adds missing layout tables; it does not modify existing `[layouts.*]` entries.
- Prefer `--target canonical` when you just want prompt rendering to work well with inferred layouts.
- Prefer `--target all` when you want one style to cover every layout name used anywhere else in `styles/`.

