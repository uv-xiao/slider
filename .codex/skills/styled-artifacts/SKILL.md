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

## Notes

- Expects `prompts/styled/*.md` to contain blocks like `## Slide N: Title`.
- Keeps intermediate slide PNGs and logs under `artifacts/<deck>/work/`.
- If a slide references `.svg` images, they are rasterized before being sent to image models (some providers reject SVG inputs).

References:
- `references/consistency-protocol.md`
- `references/pipeline-notes.md`
