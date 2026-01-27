# LLM Slides Creation Flow


I think with agents (Codex, Claude Code), artifacts creation can be automated with easy programming (skills + documents).

Let's imagine what is an automatic creation flow: provide contents in Markdown (SPEC), provide prompts about styling and layout (PROMPT), where layout can also be infered from Markdown SPEC, and LLM with skills (SKILLs) generates artifacts (ARTIFACTs)!

SPEC + PROMPT ==agent+SKILLs=> ARTIFACTs

This repo should enable the flow and more auxiliary operations.

1. SKILL management: we need skills to do replicated works like prompt generation, layout inference, reference information extraction (image, ppt, pdfs), and artifact creation (image, ppt, pdfs). All these should be stored under .codex/skills. When you miss a skill to use, find appropriate ones in skillsmp.com, and let me to download it for you.
2. PROMPT generation: we don't want to write detailed prompts, instead, we want to generate PROMPTs from some references (images, pdfs, etc). Note that, we want reusble prompts to be used for different SPEC.
3. ARTIFACT creation: now assuming we have ready PROMPT (styling + supported layouts) and SPEC, we should let agent to create ARTIFACTs. We need another kind of PROMPT, named workflow-prompt, which should be used for all artifact creation, instructing the workflow. Generally, it should analyze SPEC about the appropriate layout to use, and match with the stylish PROMPT, to generate more detailed per-artifact/-page prompt of both contents and style. Then run tools like nanobanana to create the artifacts.


File structure:

- references: images or pdfs to learn, one subfolder is one style. Should be .gitignored.
- styles: holding styles. Each style is one TOML file, with per-layout entries under `[layouts.<layout>]`.
- .codex/skills: all skills to use. 
- AGENTs.md: overall prompt to use this repo.
- and more ...

## Quickstart (local)

Generate per-slide prompts from a Markdown SPEC and a TOML style:

1. Create or edit a spec in `specs/` (see `specs/example.md`).
2. Pick a style from `styles/`:
   - `PYTHONPATH=src python3 -m slider list-styles`
3. Render prompts:
   - `PYTHONPATH=src python3 -m slider render-prompts --spec specs/example.md --style minimal --out prompts/generated/example.md`

If you prefer installing a CLI script:

- `python3 -m pip install -e .`
- `slider list-styles`
- `slider render-prompts --spec specs/example.md --style minimal --out prompts/generated/example.md`

## Notes

- `references/` and `artifacts/` are gitignored (place local images/pdfs and generated outputs there).
- Repo-wide agent guidance lives in `AGENTS.md`.
