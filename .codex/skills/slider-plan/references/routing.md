# Routing cheatsheet (v2)

## Inputs → next skill

- `materials/<deck>/...` or pasted notes → `content-prompts`
- `prompts/content/<deck>.md` → `styled-prompts`
- `prompts/styled/<deck>.md` → `styled-artifacts`

## Outputs → stop after

- Content PROMPT → `content-prompts`
- Styled PROMPT → `styled-prompts`
- Images/PDF/PPTX → `styled-artifacts`

## Style files

Preset style briefs live in `styles/*.md` (example: `styles/blueprint.md`).

Recommended style precedence:

1. Explicit user request (e.g. “use blueprint” → `styles/blueprint.md`)
2. `configs/deck.yaml` (`style:`)
3. Default to `styles/blueprint.md`

## Workdirs

All intermediates should be kept under:

- `artifacts/<deck>/work/`
