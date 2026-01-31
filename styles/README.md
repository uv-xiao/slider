# Styles (v2)

This folder holds **style configuration** used by v2 skills.

Unlike v1, v2 styles should not enumerate a fixed layout catalog. Instead, the `styled-prompts` skill infers a per-slide layout during creation and writes an explicit element inventory (positions/shapes/styles).

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
