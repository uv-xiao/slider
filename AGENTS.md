# Agent instructions (repo-level)

This repo is a scaffold for an LLM-driven slide creation workflow:

`SPEC (Markdown) + PROMPT (style/layout) -> ARTIFACTs (images/ppt/pdf)`

## Important: Use Codex as the operator (even for other agents)

This repo is designed so **concrete work is executed through Codex**, using the repo skill `slider-ops`.

If you are an external agent (e.g. Kimi Code) operating in this repo:

- Do **not** directly implement repo tasks yourself (parsing/editing styles, prompt generation, spec analysis, reference extraction, artifact generation).
- Instead, **delegate those tasks to Codex** and explicitly invoke the skill by prefixing your request with `$slider-ops`.
- Treat Codex as the single “operator” that runs commands, edits files, and produces outputs in `prompts/generated/` and `artifacts/`.

Examples of delegation instructions to Codex:

- “$slider-ops list styles, then render prompts for `specs/mydeck.md` with style `minimal`.”
- “$slider-ops create a new style `acme`, then add a `two_column_bullets` layout entry.”
- “$slider-ops read `references/acme/*` (images/pdfs/ppt), extract a reusable style prompt, and update `styles/acme.toml`.”
- “$slider-ops generate artifacts (images/ppt/pdf) into `artifacts/` after producing per-slide prompts.”

## Where things live

- `specs/`: Markdown specs (source of truth for content)
- `styles/`: reusable style TOMLs (one file per style)
- `references/`: per-style visual references (images/pdfs). This folder is gitignored.
- `prompts/`: workflow prompts and generated per-slide prompts
- `artifacts/`: generated outputs (gitignored)
- `.codex/skills/`: skills used by agents

## Typical flow

1. Put your deck content in `specs/<deck>.md`.
2. Add or pick a style in `styles/` (e.g. `styles/minimal.toml`).
3. Generate per-slide prompts:
   - Without install: `PYTHONPATH=src python3 -m slider render-prompts --spec specs/<deck>.md --style <style> --out prompts/generated/<deck>.md`
   - With install: `python3 -m pip install -e .` then `slider render-prompts --spec specs/<deck>.md --style <style> --out prompts/generated/<deck>.md`
4. Use your preferred agent/tooling (e.g., image/ppt/pdf generators) with:
   - `prompts/workflow-prompt.md`
   - `prompts/generated/<deck>.md`
