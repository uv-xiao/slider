# v2 configuration

This repo is intentionally “agent-first”: configuration is kept lightweight and is meant to guide the v2 skills:

- `.codex/skills/content-prompts/`
- `.codex/skills/styled-prompts/`
- `.codex/skills/styled-artifacts/`

## Deck preferences

Create `configs/deck.yaml` (or one per deck) to record:

- `style`: preset name or `custom`
- `audience`: beginners | intermediate | experts | executives | general
- `language`: auto | en | zh | ja | ...
- `dimensions`: texture/mood/typography/density (when `style: custom`)

Schema reference:

- `.codex/skills/styled-prompts/references/config/preferences-schema.md`

## How v2 skills use it

- `content-prompts`: uses `audience`, `language`, and `density` to decide splitting and per-page intent.
- `styled-prompts`: uses `style`/`dimensions` to construct the style constraints and choose appropriate visual language.

## Preset styles

Preset briefs: `styles/presets/<style>.md`

Preset configs: `styles/<style>.toml`

Keep the config in git so the workflow is reproducible.
