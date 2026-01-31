# Agent instructions (repo-level)

This repo is a scaffold for an LLM-driven slide creation workflow:

`SPEC (Markdown) + PROMPT (style/layout) -> ARTIFACTs (images/ppt/pdf)`

## Important: Delegate to Codex (even for other agents)

This repo is designed so **all concrete work is executed through Codex**.

### Two modes of delegation

**1. Operations (use v2 skills):**

For day-to-day tasks, use the v2 skills:

- Do **not** directly implement operational tasks yourself (content planning, slide design, artifact generation).
- Instead, explicitly invoke the relevant skill.

Examples:
- "$content-prompts read `materials/mydeck/` and produce `prompts/content/mydeck.md`."
- "$styled-prompts convert `prompts/content/mydeck.md` + `styles/acme.toml` into `prompts/styled/mydeck.md`."
- "$styled-artifacts generate images + PDF + PPTX from `prompts/styled/mydeck.md` into `artifacts/mydeck/work/`."

**2. Feature Evolution (delegate freely to Codex):**

For adding new capabilities, extending workflows, or modifying the repo's architecture:

- **Delegate to Codex without the `$slider-ops` skill wrapper** so Codex can freely use any skills (e.g., `create-plan`, `Bash`, `Read`, etc.).
- The outer agent should engage in **interactive discussion** with Codex about plans, approach, and design decisions.
- Codex drives the implementation using appropriate skills.

Examples:
- "Codex, let's add support for a new output format `docx`. First, discuss the approach with me."
- "Codex, extend the style TOML schema to support `animation_hints` per layout. What's your plan?"
- "Codex, refactor the prompt rendering logic to support conditional layouts. Let's iterate on the design."

## Where things live

- `materials/`: raw notes/images/source docs
- `configs/`: v2 deck preferences (audience/language/style/dimensions)
- `prompts/content/`: per-page content prompts (v2)
- `prompts/styled/`: per-page styled prompts (v2; used for image/PDF/PPT generation)
- `styles/`: style configs (TOML; v2, no fixed layout catalog)
- `references/`: per-style visual references (images/pdfs). This folder is gitignored.
- `artifacts/`: generated outputs + per-deck workdirs (gitignored)
- `.codex/skills/`: skills used by agents

## Typical flow

### Recommended (v2 / agentic)

1. Put raw material in `materials/<deck>/...`.
2. Generate per-page content prompts in `prompts/content/<deck>.md` (skill-driven planning, density checks).
3. Convert to styled prompts in `prompts/styled/<deck>.md` using a style config from `styles/<style>.toml`.
4. Generate slide images + PDF/PPTX into `artifacts/<deck>/` (keep intermediates in `artifacts/<deck>/work/`).

### Archived (v1)

Legacy v1 components live under `archieve/v1/`.
