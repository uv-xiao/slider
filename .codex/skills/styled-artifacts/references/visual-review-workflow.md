# Visual review workflow (adapted from archived v1)

Condensed from:

- `archieve/v1/.codex/skills/scientific-slides/references/visual_review_workflow.md`

## Rule

Never “review” a deck by reading a PDF as text. Always review slide renderings as images.

## Recommended workflow

1. Generate slides to images (`artifacts/<deck>/work/slides/*.png`).
2. Assemble `PDF` / `PPTX`.
3. Inspect:
   - quick overview pass (scan for obvious outliers)
   - detailed pass (text overflow, overlaps, legibility, alignment)
   - cross-slide consistency (fonts, margins, colors, icon styles)
4. If issues:
   - fix the styled prompt for the specific slide(s)
   - regenerate only those slides
   - rebuild PDF/PPTX

## Common issues checklist

- text too small / dense
- clipped text at edges
- overlaps between boxes/arrows/text
- inconsistent icon style across slides
- low contrast (projector risk)
- figure/table not highlighted with the intended insight

