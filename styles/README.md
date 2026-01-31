# Styles (v2)

This folder holds **Markdown style briefs** used by v2 skills.

Unlike v1, v2 styles should not enumerate a fixed layout catalog. Instead, the `styled-prompts` skill infers a per-slide layout during creation and writes an explicit element inventory (positions/shapes/styles).

## Presets

Preset style briefs live in `styles/*.md` (e.g. `styles/blueprint.md`, `styles/corporate.md`).

## Recommended format (for `styles/<style>.md`)

Keep it human-readable and “prompt-ready”. A good style brief usually includes:

- `# <style-name>` + a one-line tagline
- `## Design Aesthetic`
- `## Background` (color + texture)
- `## Typography` (headline/body guidance)
- `## Color Palette` (table with hex codes and roles)
- `## Visual Elements` (icon/illustration/diagram language)
- `## Style Rules` (Do / Don’t)
- `## Best For`

Optional (but useful):

- `## Dimensions` (texture/mood/typography/density), using the dimension vocabulary:
  - `.codex/skills/styled-prompts/references/dimensions/presets.md`
  - `.codex/skills/styled-prompts/references/dimensions/*.md`

## How to use

1. Choose a preset style file, e.g. `styles/blueprint.md`.
2. Set `style: blueprint` in `configs/deck.yaml`.
3. When invoking `$styled-prompts`, pass the style brief file and treat it as constraints (palette/typography/shape language), not as a layout enum.
