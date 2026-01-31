# LLM Slide Deck Workflow (Agentic)

This repo is a scaffold for an agent-driven slide workflow that keeps *planning* and *design decisions* inside agent skills, instead of hard-coding page-splitting and layout matching in scripts.

## Recommended flow (v2)

The core idea is to split the problem into two prompt transformations, then generate artifacts:

1) **Material → Content Prompt** (content density + intent → per-page plan)
- Input: `materials/<deck>/...` (raw notes, images, references)
- Output: `prompts/content/<deck>.md`
- Skill: `.codex/skills/content-prompts/`

2) **Content Prompt → Styled Prompt** (design + layout inference at creation time)
- Input: `prompts/content/<deck>.md` + `styles/<style>.toml` (style config)
- Output: `prompts/styled/<deck>.md`
- Skill: `.codex/skills/styled-prompts/`

3) **Styled Prompt → Images + PDF/PPTX**
- Input: `prompts/styled/<deck>.md`
- Output workdir: `artifacts/<deck>/work/` (intermediate prompts, images, logs)
- Final outputs: `artifacts/<deck>/<deck>.pdf` and `artifacts/<deck>/<deck>.pptx`
- Skill/tooling: `.codex/skills/scientific-slides/` (and/or `.codex/skills/baoyu-slide-deck/`)

### Why this is better than v1

- No redundant “layout matching” step: the styling skill can infer the best layout *while* placing content.
- Fewer built-in layouts: styles focus on visual identity and constraints; page structure is decided per slide.
- Workdir keeps everything reproducible and debuggable (`artifacts/<deck>/work/`), without polluting git history.

## Legacy flow (v1 / slider CLI)

The original slider flow is still available for deterministic scaffolding:

`SPEC (specs/*.md) + STYLE (styles/*.toml) -> slider render-prompts -> prompts/generated/*.md`

## Repo structure

- `materials/`: raw source material (notes, images, scratch docs)
- `specs/`: structured Markdown specs (legacy flow input)
- `styles/`: style configs (TOML; used by both flows)
- `prompts/content/`: per-page content prompts (v2)
- `prompts/styled/`: per-page styled prompts (v2; input to artifact generation)
- `prompts/generated/`: per-slide prompts rendered from specs (legacy)
- `prompts/workflow-prompt.md`: reusable workflow prompt template (legacy)
- `.codex/skills/`: agent skills (planning, design, generation, validation)
- `artifacts/`: generated workdirs and final outputs (gitignored)
- `references/`: optional style references (gitignored; keep only README.md in git)

## Quickstart (artifact generation)

Install runtime deps (recommended):

- `pixi install`

Generate PDF/PPTX from a styled prompts file:

- `OPENROUTER_API_KEY=... python3 .codex/skills/scientific-slides/scripts/slider_prompts_to_artifacts.py --prompts prompts/styled/<deck>.md --out-dir artifacts/<deck> --pdf artifacts/<deck>/<deck>.pdf --pptx artifacts/<deck>/<deck>.pptx`

## Notes

- `references/` and `artifacts/` are gitignored (place local images/pdfs and generated outputs there).
- Repo-wide agent guidance lives in `AGENTS.md`.
