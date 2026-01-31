# LLM Slide Deck Workflow (Agentic)

This repo is a scaffold for an agent-driven slide workflow that keeps *planning* and *design decisions* inside agent skills, instead of hard-coding page-splitting and layout matching in scripts.

## Recommended flow (v2)

The core idea is to split the problem into two prompt transformations, then generate artifacts:

1) **Material → Content Prompt** (content density + intent → per-page plan)
- Input: `materials/<deck>/...` (raw notes, images, references)
- Output: `prompts/content/<deck>.md`
- Skill: `.codex/skills/content-prompts/`

2) **Content Prompt → Styled Prompt** (design + layout inference at creation time)
- Input: `prompts/content/<deck>.md` + `styles/<style>.md` (style brief)
- Output: `prompts/styled/<deck>.md`
- Skill: `.codex/skills/styled-prompts/`
  - The styled prompt is design-complete: element inventory + positions + shapes, and may add icons/illustrations/tables/diagrams to make content more intuitive.

3) **Styled Prompt → Images + PDF/PPTX**
- Input: `prompts/styled/<deck>.md`
- Output workdir: `artifacts/<deck>/work*/` (intermediate prompts, images, logs)
- Final outputs: `artifacts/<deck>/<deck>.pdf` and `artifacts/<deck>/<deck>.pptx`
- Skill: `.codex/skills/styled-artifacts/`

### Why this is better than v1

- No redundant “layout matching” step: the styling skill can infer the best layout *while* placing content.
- Fewer built-in layouts: styles focus on visual identity and constraints; page structure is decided per slide.
- Workdir keeps everything reproducible and debuggable (`artifacts/<deck>/work*/`), without polluting git history.

## Usage

This repo is designed to be driven by agent skills (see `AGENTS.md`). When a user asks for “generate prompts” or “export PDF/PPTX”, start with the orchestrator skill:

- `$slider-plan`: produces a plan (in the `create-plan` template) that sequences the needed v2 skills.

Then run the individual skills as needed:

- `$content-prompts` → writes `prompts/content/<deck>.md`
- `$styled-prompts` → writes `prompts/styled/<deck>.md`
- `$styled-artifacts` → writes `artifacts/<deck>/...`

### Starting from different inputs

- If you have raw sources: start at `materials/<deck>/...` → `$content-prompts`
- If you already have `prompts/content/<deck>.md`: start at `$styled-prompts`
- If you already have `prompts/styled/<deck>.md`: start at `$styled-artifacts`

### Style selection

V2 styles are **Markdown briefs** in `styles/*.md` (example: `styles/blueprint.md`).

Recommended:

- Set `style: <name>` in `configs/deck.yaml` (example: `style: blueprint`)
- Pass `styles/<name>.md` to `$styled-prompts` when styling

See `styles/README.md` for the suggested style brief format.

### Prompt review policy (important)

Keep generation cheap:

- Review happens on prompts (`prompts/content/*` and `prompts/styled/*`)
- Avoid expensive “regenerate + review” loops on final artifacts

## Setup (artifact rendering)

### Dependencies

Recommended: use Pixi:

- `pixi install`

Alternatively, install the Python deps used by the artifact scripts:

- `pip install requests Pillow python-pptx`

### API key

Artifact rendering calls OpenRouter for image generation. Provide an API key via either:

- env var: `OPENROUTER_API_KEY=...`
- or a local file: `.OPENROUTER_API_KEY` at repo root (gitignored)

## Render artifacts (CLI)

Given a styled prompts file `prompts/styled/<deck>.md`, generate images + PDF + PPTX:

- `OPENROUTER_API_KEY=... python3 .codex/skills/styled-artifacts/scripts/styled_prompts_to_artifacts.py --prompts prompts/styled/<deck>.md --workdir artifacts/<deck>/work --pdf artifacts/<deck>/<deck>.pdf --pptx artifacts/<deck>/<deck>.pptx`

### Existing output behavior (workdir versioning)

To avoid clobbering previous outputs, the script auto-versions the workdir:

- If `artifacts/<deck>/work` exists, it writes to `artifacts/<deck>/work-2`, `work-3`, ...
- For iterative edits where you want to keep prior slide images, add `--reuse-workdir`

### Regenerate specific slides (cheap iteration)

After editing `prompts/styled/<deck>.md`, regenerate only the impacted slides:

- `OPENROUTER_API_KEY=... python3 .codex/skills/styled-artifacts/scripts/styled_prompts_to_artifacts.py --prompts prompts/styled/<deck>.md --workdir artifacts/<deck>/work --reuse-workdir --only 7`
- `... --only 2,5,8`
- `... --only 5-8`

If you also pass `--pdf`/`--pptx` with `--only`, the script expects the other slide images to already exist in the same reused workdir.

## Prompt formats (v2)

### Content prompts (`prompts/content/<deck>.md`)

One section per page:

- `## Page N: <title>`
- `Intent`, `Must include`, `Suggested representation`, `Assets`, `Notes / TODO`

See `.codex/skills/content-prompts/references/content-prompt-template.md`.

### Styled prompts (`prompts/styled/<deck>.md`)

1) **Deck-level header (required)**: put a global style/formatting contract *before* the first slide (palette roles, typography feel, reusable components, icon/illustration rules).

2) One section per slide:

- `## Slide N: <title>`
- layout decision (free-form)
- a full element inventory (bbox + content + style for every element)
- asset list (local paths / URLs)

See `.codex/skills/styled-prompts/references/element-spec-template.md`.

## Archived v1

Legacy v1 components (slider CLI, layout catalogs, and earlier artifact skills) are kept under `archieve/v1/` for reference.

## Repo structure

- `materials/`: raw source material (notes, images, scratch docs)
- `configs/`: v2 deck preferences (audience/language/style/dimensions)
- `styles/`: style briefs (Markdown; v2, no fixed layout catalog)
- `prompts/content/`: per-page content prompts (v2)
- `prompts/styled/`: per-page styled prompts (v2; input to artifact generation)
- `.codex/skills/`: agent skills (planning, design, generation, validation)
- `artifacts/`: generated workdirs and final outputs (gitignored)
- `references/`: optional style references (gitignored; keep only README.md in git)

Legacy v1 folders (e.g. `specs/`, `prompts/generated/`, older skills) are under `archieve/v1/`.

## Notes

- `references/` and `artifacts/` are gitignored (place local images/pdfs and generated outputs there).
- Repo-wide agent guidance lives in `AGENTS.md`.
