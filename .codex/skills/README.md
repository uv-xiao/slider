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
- `slider-plan`: plan/orchestrate which skills to run for a user request (plan-only; use before generating prompts/artifacts)
- `content-prompts`: convert raw material into per-page content prompts (`prompts/content/*`)
- `styled-prompts`: convert content prompts into design-complete prompts (`prompts/styled/*`)
- `styled-artifacts`: generate images + PDF/PPTX from `prompts/styled/*` into `artifacts/<deck>/work/`

Archived (v1) skills live under `archieve/v1/.codex/skills/`.
