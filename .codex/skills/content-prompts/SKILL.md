---
name: content-prompts
description: "Convert raw material into per-page Content PROMPTs by analyzing content density, intent, and slide usage. Outputs prompts/content/<deck>.md. Use when the user has notes/materials and wants a well-planned per-page content prompt before styling."
---

# Content Prompts (Material → Content PROMPT)

## Goal

Turn raw material (notes, markdown, images, links) into a **per-page Content PROMPT** file that:

- preserves *all* important information (no silent dropping)
- optimizes logic and narrative flow
- controls density (split/merge pages intentionally)
- adds “what this slide is for” (live talk vs. document vs. training)
- captures requirements for non-text representations (tables, diagrams, code, charts)

## Inputs

- `materials/<deck>/...` (preferred) or a provided Markdown blob
- Optional constraints: target audience, target slide count, talk type, time limit
- Optional: deck preferences under `configs/deck.yaml` (audience/language/style/dimensions)

## Output

Write to: `prompts/content/<deck>.md`

Format (recommended):

- A short header with deck metadata (audience, purpose, constraints)
- Then one section per page:
  - `## Page N: <title>`
  - **Intent**: why this page exists
  - **Must include**: all facts/claims/code/images that must appear
  - **Optional**: items that can be trimmed if density is too high
  - **Suggested representations**: bullets vs. diagram vs. table vs. code vs. illustration vs. iconography
  - **Assets**: local file paths / URLs, captions, attribution notes

Templates and references:
- `references/content-prompt-template.md`
- `references/analysis-framework.md`
- `references/content-rules.md`

## Density and splitting guidance

- If a page exceeds “one-screen readability”, split into `Page N` and `Page N (cont.)`.
- Prefer splitting by phases and intent boundaries:
  - setup → execution → results → lessons
  - topic boundary
  - step sequence
  - before/after comparison
  - example vs. takeaway

For a more detailed checklist, see:
- `references/content-prompt-template.md`
- `references/analysis-framework.md`
- `references/content-rules.md`
- `references/splitting-guide.md`
- `references/common-pitfalls.md`

## Suggested workflow (phases)

Use a consistent phase checklist (inspired by the planning/validation patterns in archived v1 skills):

1. **Setup & analyze**
   - Identify target: live talk vs shareable doc vs training.
   - Identify audience level and target length (time or slide count).
   - Identify content types present (code, tables, diagrams, screenshots).
2. **Draft page plan**
   - Propose page titles as takeaways.
   - Decide per-page representation (bullets vs diagram vs table vs code).
3. **Density check**
   - Split pages that have multiple intents or competing representations.
   - Merge pages that are too sparse and share the same intent.
4. **Consistency check**
   - Terminology consistency, no unexplained acronyms, consistent naming.
5. **Coverage check**
   - Ensure every important source item is captured under “Must include”.

Copy/paste checklist:

```

## Review gate (required)

Do not proceed to `styled-prompts` until the content prompt passes:

- No silent dropping (everything important is in “Must include” somewhere)
- Each page has exactly one intent and a clear primary representation
- Any missing data for tables/figures is explicitly marked as TODO
Content PROMPT Progress:
- [ ] Setup & analyze (audience, use case, length)
- [ ] Draft page plan (titles + representations)
- [ ] Density pass (split/merge)
- [ ] Consistency pass (terms, acronyms, naming)
- [ ] Coverage pass (no silent dropping)
```

## Guardrails

- Do not decide final visual layout here (that’s the styling step).
- Do not invent facts; if a source is ambiguous, mark it as a TODO/question.
- Keep titles short and information-rich.

## Modification & iteration

Treat `prompts/content/<deck>.md` as the single source of truth for planning.

- **Edit a page**: update the page’s “Must include” and “Suggested representation”.
- **Split a page**: duplicate the page section into `Page N` and `Page N (cont.)`, then re-check density and intent.
- **Merge pages**: merge only if they share one intent and one primary representation.
- After edits, re-run the “Review gate” checklist before moving on to styling.

## Completion behavior (required)

When this skill is triggered:

1. **Do only this step**: produce/update `prompts/content/<deck>.md`.
2. **Do not run downstream steps** (no `$styled-prompts`, no `$styled-artifacts`, no rendering sanity-checks) unless the user explicitly requested them in the same message.
3. **End your response with recommended next steps** (options + commands to run next).

Recommended next steps (include this block in your response):

- **Review gate (required before styling)**: confirm the Content PROMPT passes the checklist in this skill.
- **Next (create Styled PROMPT)**: run `$styled-prompts` on the generated file.
  - Style selection options:
    - Use `configs/deck.yaml` (`style:`) if present
    - Or pick a preset: `styles/blueprint.md`, `styles/chalkboard.md`, `styles/sketch-notes.md`, ...
  - Recommended invocation:
    - `$styled-prompts convert prompts/content/<deck>.md + styles/<style>.md into prompts/styled/<deck>.md.`

If the user requested only a **sample** (e.g. 4 pages), recommend validating the sample first, then rerunning this skill for full coverage.
