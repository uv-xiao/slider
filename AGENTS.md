# Agent instructions (repo-level)

This repo is a scaffold for an LLM-driven slide creation workflow:

`SPEC (Markdown) + PROMPT (style/layout) -> ARTIFACTs (images/ppt/pdf)`

## Important: Delegate to Codex (even for other agents)

This repo is designed so **all concrete work is executed through Codex**.

### Two modes of delegation

**1. Operations (use `$slider-ops`):**

For day-to-day tasks using existing slider features, use the repo skill `slider-ops`:

- Do **not** directly implement operational tasks yourself (parsing/editing styles, prompt generation, spec analysis, reference extraction, artifact generation).
- Instead, **delegate to Codex via `$slider-ops`** and explicitly invoke the skill.

Examples:
- "$slider-ops list styles, then render prompts for `specs/mydeck.md` with style `minimal`."
- "$slider-ops create a new style `acme`, then add a `two_column_bullets` layout entry."
- "$slider-ops read `references/acme/*` (images/pdfs/ppt), extract a reusable style prompt, and update `styles/acme.toml`."
- "$slider-ops generate artifacts (images/ppt/pdf) into `artifacts/` after producing per-slide prompts."

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
- `prompts/content/`: per-page content prompts (v2)
- `prompts/styled/`: per-page styled prompts (v2; used for image/PDF/PPT generation)
- `specs/`: Markdown specs (legacy; deterministic scaffold)
- `styles/`: style configs (TOML; used by both v1 and v2)
- `references/`: per-style visual references (images/pdfs). This folder is gitignored.
- `prompts/`: workflow prompts and generated per-slide prompts
- `artifacts/`: generated outputs + per-deck workdirs (gitignored)
- `.codex/skills/`: skills used by agents

## Typical flow

### Recommended (v2 / agentic)

1. Put raw material in `materials/<deck>/...`.
2. Generate per-page content prompts in `prompts/content/<deck>.md` (skill-driven planning, density checks).
3. Convert to styled prompts in `prompts/styled/<deck>.md` using a style config from `styles/<style>.toml`.
4. Generate slide images + PDF/PPTX into `artifacts/<deck>/` (keep intermediates in `artifacts/<deck>/work/`).

### Legacy (v1 / slider CLI)

1. Put your deck content in `specs/<deck>.md`.
2. Pick a style in `styles/` (e.g. `styles/minimal.toml`).
3. Generate per-slide prompts:
   - Without install: `PYTHONPATH=src python3 -m slider render-prompts --spec specs/<deck>.md --style <style> --out prompts/generated/<deck>.md`
   - With install: `python3 -m pip install -e .` then `slider render-prompts --spec specs/<deck>.md --style <style> --out prompts/generated/<deck>.md`
4. Generate artifacts from `prompts/generated/<deck>.md` using `.codex/skills/scientific-slides/`.
