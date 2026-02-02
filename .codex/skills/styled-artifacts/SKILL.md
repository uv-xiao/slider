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

Important clarification:

- Once you have an editable PPTX output file (e.g. `artifacts/<deck>/<deck>.editable.pptx`), you are **done**.
- “Rebuild” is only for **iteration**:
  - If you want the PPTX to remain reproducible from HTML/CSS, edit the HTML sources and rerun the builder.
  - If you just want to tweak content/layout manually, open the PPTX in PowerPoint/Keynote and edit directly (no rebuild needed).


Recommended approach:

1. Use the styled prompt (`prompts/styled/<deck>.md`) as source of truth for slide geometry and content.
2. Create one HTML file per slide under `artifacts/<deck>/work/pptx-html/` using the rules in `.codex/skills/pptx/html2pptx.md` (body size `720pt × 405pt`).
3. Use `pptx` skill’s html2pptx workflow to convert HTML slides into `artifacts/<deck>/<deck>.editable.pptx`.
4. Run `.codex/skills/pptx/scripts/thumbnail.py` to visually validate and iterate until there is no cutoff/overlap.


Quality note:

- Editable PPTX can look less “styled” than image-rendered PDF/PPTX, because it is limited by web-safe fonts and PPTX element primitives.
- If fidelity is unacceptable, iterate on the **Styled PROMPT** first, then use `$pptx` to redesign the HTML/CSS (or switch to a template-based PPTX workflow).

References:
- `references/consistency-protocol.md`
- `references/pipeline-notes.md`

## Completion behavior (required)

When this skill is triggered:

1. **Do only this step**: render the artifacts the user explicitly requested (images / PDF / image-PPTX).
2. **Do not invoke other skills automatically** (e.g. `$pptx` for editable PPTX) unless explicitly requested.
3. **End your response with recommended next steps** (options + commands to run next).

Recommended next steps (include this block in your response):

- **Outputs**: point to the workdir and final artifact paths.
- **Iterate cheaply** (after editing `prompts/styled/<deck>.md`):
  - `OPENROUTER_API_KEY=... python3 .codex/skills/styled-artifacts/scripts/styled_prompts_to_artifacts.py --prompts prompts/styled/<deck>.md --workdir artifacts/<deck>/work --reuse-workdir --only 7`
- **Editable PPTX** (if requested): invoke `$pptx` and follow `.codex/skills/pptx/html2pptx.md`.
  - If you already have `artifacts/<deck>/<deck>.editable.pptx`, **stop here**.
  - Rebuild only if you’re iterating via HTML/CSS (otherwise just edit the PPTX directly in PowerPoint).
