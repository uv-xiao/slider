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

## Output

Write to: `prompts/content/<deck>.md`

Format (recommended):

- A short header with deck metadata (audience, purpose, constraints)
- Then one section per page:
  - `## Page N: <title>`
  - **Intent**: why this page exists
  - **Must include**: all facts/claims/code/images that must appear
  - **Optional**: items that can be trimmed if density is too high
  - **Suggested representations**: bullets vs. diagram vs. table vs. code vs. illustration
  - **Assets**: local file paths / URLs, captions, attribution notes

## Density and splitting guidance

- If a page exceeds “one-screen readability”, split into `Page N` and `Page N (cont.)`.
- Prefer splitting by:
  - topic boundary
  - step sequence
  - before/after comparison
  - example vs. takeaway

## Guardrails

- Do not decide final visual layout here (that’s the styling step).
- Do not invent facts; if a source is ambiguous, mark it as a TODO/question.
- Keep titles short and information-rich.

