# Styles (v2)

This folder holds **style configuration** used by v2 skills.

Unlike v1, v2 styles should not enumerate a fixed layout catalog. Instead, the `styled-prompts` skill infers a per-slide layout during creation and writes an explicit element inventory (positions/shapes/styles).

## Preset styles

Preset style briefs live in `styles/presets/*.md`.

Preset style configs live in `styles/*.toml` (e.g. `styles/blueprint.toml`, `styles/corporate.toml`).

Recommended usage:

- Set `style: blueprint` in `configs/deck.yaml`
- Then pass `styles/blueprint.toml` to `styled-prompts`

Minimal suggested schema:

```toml
[GENERAL]
style = "minimal" # optional
style_prompt = """...global visual identity..."""

[DIMENSIONS]
# Optional: use the baoyu-style dimension system to describe the visual language.
# See:
# - .codex/skills/styled-prompts/references/dimensions/presets.md
# - .codex/skills/styled-prompts/references/dimensions/*.md
texture = "clean"
mood = "professional"
typography = "geometric"
density = "balanced"

[TOKENS]
# Optional: common colors, stroke widths, radii, typography hints, etc.
```
