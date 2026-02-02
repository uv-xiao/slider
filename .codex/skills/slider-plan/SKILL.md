---
name: slider-plan
description: "Plan the v2 slider workflow end-to-end by selecting which repo skills to run (content-prompts, styled-prompts, styled-artifacts) based on the user’s starting input (materials or existing prompts) and requested output (content prompt, styled prompt, images, PDF, PPTX). Use when a user asks to generate prompts or render/export slide artifacts in a specific format."
---

# Slider Plan (Orchestrator)

## Goal

Produce a **plan only** (no file edits, no rendering) that routes the user request to the right v2 skill(s):

- `content-prompts` → material → `prompts/content/<deck>.md`
- `styled-prompts` → content prompt + style brief → `prompts/styled/<deck>.md`
- `styled-artifacts` → styled prompt → images + `artifacts/<deck>/<deck>.pdf` / image-PPTX `artifacts/<deck>/<deck>.pptx`
- `pptx` → styled prompt → **editable** PPTX `artifacts/<deck>/<deck>.editable.pptx` (HTML→PPTX workflow + thumbnail validation)

The plan must be written in the same format as the `create-plan` skill template.

## Routing

Decide the starting point from the user’s input:

- Raw notes / folder / “material” → run `content-prompts`
- Already has `prompts/content/<deck>.md` → start at `styled-prompts`
- Already has `prompts/styled/<deck>.md` → start at `styled-artifacts`

Decide the stopping point from the requested output:

- Wants **Content PROMPT** → stop after `content-prompts`
- Wants **Styled PROMPT** → stop after `styled-prompts`
- Wants **PDF / images / image-PPTX** → include `styled-artifacts`
- Wants **editable PPTX** → include `pptx` after `styled-prompts` (and optionally after `styled-artifacts` if they also want slide PNGs/PDF)

## Style selection (v2)

- If the user names a style, use `styles/<style>.md`.
- Otherwise, use `configs/deck.yaml` (`style:`) if present.
- If neither is available, default to `styles/blueprint.md` (or ask 1 question if the choice matters).

## Review policy (required)

Keep generation cheap:

- Review happens on **prompts** (`prompts/content/*` and/or `prompts/styled/*`).
- Do **not** plan “regenerate + review” loops for final artifacts.

## Output format

Output only a plan, using the exact template structure:

- `# Plan`
- `## Scope`
- `## Action items` (include the exact skill invocations and file paths)
- `## Open questions` (max 3; ask only if blocking)

## References

- Routing cheatsheet: `references/routing.md`
- Example plans: `references/examples.md`

## Completion behavior (required)

When this skill is triggered:

1. **Do only this step**: output a plan (no file edits, no rendering).
2. The plan must include the **exact next skill invocations** and any **CLI commands** needed.
3. Do not execute the plan steps automatically.
