# Styles (v2)

This folder holds **style configuration** used by v2 skills.

Unlike v1, v2 styles should not enumerate a fixed layout catalog. Instead, the `styled-prompts` skill infers a per-slide layout during creation and writes an explicit element inventory (positions/shapes/styles).

Minimal suggested schema:

```toml
[GENERAL]
style_prompt = """...global visual identity..."""

[TOKENS]
# Optional: common colors, stroke widths, radii, typography hints, etc.
```

