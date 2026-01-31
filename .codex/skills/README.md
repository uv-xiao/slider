# Codex skills

Put agent skills under `.codex/skills/`.

Suggested skill categories for this repo:

- content planning (from raw material)
- design/styling (from content prompts + style config)
- prompt generation (from references)
- reference extraction (from images/pdfs/ppt)
- artifact creation (image/ppt/pdf)

If you're missing a skill, search for one (e.g. skillsmp.com) and add it here.

Repo skills:
- `slider-ops`: day-to-day style/spec/prompt operations
- `style-evolve`: add missing `[layouts.*]` entries to a style TOML
- `spec-structurer`: convert unstructured Markdown into a multi-slide SPEC
- `scientific-slides`: generate final slide artifacts (PDF/PPTX) from `prompts/generated/*`
- `baoyu-slide-deck`: end-to-end slide deck generation (outline → prompts → images → PDF/PPTX)
- `content-prompts`: convert raw material into per-page content prompts (`prompts/content/*`)
- `styled-prompts`: convert content prompts into design-complete prompts (`prompts/styled/*`)
