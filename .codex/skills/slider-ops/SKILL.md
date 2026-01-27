---
name: slider-ops
description: "Operate the /slider repo end-to-end: list/create/update/delete slide styles (styles/*.toml), manage per-style layout tables under [layouts.*], scaffold specs (specs/*.md), and render per-slide prompts (prompts/generated/*) using the bundled slider_ops script and/or the slider CLI. Use when a user asks to create/manage styles or layouts, generate prompts from a Markdown SPEC, or otherwise run the slider workflow so Codex should execute commands/edits instead of the user."
---

# Slider Ops

## Overview

Use this skill to translate a user request into concrete actions in this repo (edit `styles/*.toml`, create/update `specs/*.md`, and generate `prompts/generated/*.md`) by running the bundled automation script and/or the `slider` CLI.

## Quick start

- List available styles:
  - `python3 .codex/skills/slider-ops/scripts/slider_ops.py styles list`
- Render prompts for a deck:
  - `python3 .codex/skills/slider-ops/scripts/slider_ops.py prompts render --spec specs/example.md --style minimal --out prompts/generated/example.md`

If the user wants an installed CLI, install once then use `slider ...`:

- `python3 -m pip install -e .`
- `slider list-styles`
- `slider render-prompts --spec specs/example.md --style minimal --out prompts/generated/example.md`

## Tasks

### Styles (create/manage)

- List: `python3 .codex/skills/slider-ops/scripts/slider_ops.py styles list`
- Show one: `python3 .codex/skills/slider-ops/scripts/slider_ops.py styles show minimal`
- Create a style file: `python3 .codex/skills/slider-ops/scripts/slider_ops.py styles create my-style --clone minimal`
- Delete a style file: `python3 .codex/skills/slider-ops/scripts/slider_ops.py styles delete my-style`

### Layouts (within a style)

- List layouts: `python3 .codex/skills/slider-ops/scripts/slider_ops.py layouts list minimal`
- Create/update a layout:
  - `python3 .codex/skills/slider-ops/scripts/slider_ops.py layouts upsert minimal title_bullets --clone title_bullets`
  - Provide overrides via files: `--description @desc.txt --prompt @prompt.txt`
- Delete a layout: `python3 .codex/skills/slider-ops/scripts/slider_ops.py layouts delete minimal title_bullets`

When the user wants “a new style from references”, first inspect `references/<style>/` (gitignored) and summarize the visual constraints into `[GENERAL].style_prompt`, then create the style file and add/update its layouts.

### Specs (Markdown)

- Create a starter spec:
  - `python3 .codex/skills/slider-ops/scripts/slider_ops.py spec init --out specs/mydeck.md --title "My Deck" --slides "Intro,Problem,Solution,Next steps"`
- Edit specs via normal file edits (`apply_patch`) when the user provides content.

### Prompts (render)

- Render per-slide prompts:
  - `python3 .codex/skills/slider-ops/scripts/slider_ops.py prompts render --spec specs/mydeck.md --style minimal --out prompts/generated/mydeck.md`

## Guardrails

- Prefer writing generated files into `prompts/generated/` and artifacts into `artifacts/` (both gitignored).
- If you change `styles/*.toml`, keep style names stable (they are referenced by name in prompts).
- If a user asks for “just do it”, run the commands and update the repo; do not ask them to run `slider` themselves.
