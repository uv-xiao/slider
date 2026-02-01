---
name: styled-artifacts
description: "Generate slide images and final PDF/PPTX from v2 styled prompts (prompts/styled/*.md), storing intermediates in artifacts/<deck>/work/. Use when the user asks to render/generate/export slides from a Styled PROMPT into images/PDF/PPTX."
---

# Styled Artifacts (Styled PROMPT → Images + PDF/PPTX)

## Quick start

Generate all artifacts into a per-deck workdir:

- `OPENROUTER_API_KEY=... python3 .codex/skills/styled-artifacts/scripts/styled_prompts_to_artifacts.py --prompts prompts/styled/<deck>.md --workdir artifacts/<deck>/work --pdf artifacts/<deck>/<deck>.pdf --pptx artifacts/<deck>/<deck>.pptx`

## Workflow (recommended)

1. Generate slide images into `artifacts/<deck>/work/slides/`.
2. Assemble PDF/PPTX.
3. Keep generation cheap: review happens on prompts (content/styled), not on final artifacts.

## Existing output behavior (workdir versioning)

To avoid clobbering prior outputs, the renderer auto-versions the workdir:

- If `--workdir artifacts/<deck>/work` already exists, it will write to `artifacts/<deck>/work-2`, `work-3`, ...
- For iterative edits where you want to keep prior slide images, pass `--reuse-workdir`.

## Modification & iteration (cheap)

### Regenerate specific slides

Edit `prompts/styled/<deck>.md`, then regenerate only the affected slide numbers:

- `OPENROUTER_API_KEY=... python3 .codex/skills/styled-artifacts/scripts/styled_prompts_to_artifacts.py --prompts prompts/styled/<deck>.md --workdir artifacts/<deck>/work --reuse-workdir --only 7`
- `... --only 2,5,8`
- `... --only 5-8`

If you pass `--pdf/--pptx` together with `--only`, the script expects the other slide images to already exist in the same reused workdir.

### Add / delete / reorder slides

- Keep slide numbers unique: `## Slide N: ...` must not repeat.
- When inserting a slide, renumber subsequent slides and regenerate the affected range with `--only`.
- When deleting a slide, renumber subsequent slides and regenerate the affected range with `--only`.

## Notes

- Expects `prompts/styled/*.md` to contain blocks like `## Slide N: Title`.
- Keeps intermediate slide PNGs and logs under `artifacts/<deck>/work/`.
- If a slide references `.svg` images, they are rasterized before being sent to image models (some providers reject SVG inputs).
- PPTX outputs:
  - **Image PPTX** (`--pptx`): slide images packaged into a PPTX (fast; not truly editable).

## Editable PPTX (use `$pptx` skill)

For an actually-editable PPTX (native text boxes, tables, shapes), use the `pptx` skill’s full workflow (HTML→PPTX and thumbnail validation). `styled-artifacts` intentionally does not attempt to auto-generate editable PPTX via a single script.

Recommended approach:

1. Use the styled prompt (`prompts/styled/<deck>.md`) as source of truth for slide geometry and content.
2. Create one HTML file per slide under `artifacts/<deck>/work/pptx-html/` using the rules in `.codex/skills/pptx/html2pptx.md` (body size `720pt × 405pt`).
3. Use `pptx` skill’s html2pptx workflow to convert HTML slides into `artifacts/<deck>/<deck>.editable.pptx`.
4. Run `.codex/skills/pptx/scripts/thumbnail.py` to visually validate and iterate until there is no cutoff/overlap.

References:
- `references/consistency-protocol.md`
- `references/pipeline-notes.md`
