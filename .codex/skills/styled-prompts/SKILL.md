---
name: styled-prompts
description: "Convert per-page Content PROMPTs into design-complete Styled PROMPTs using a style config, inferring the best layout per page during creation. Outputs prompts/styled/<deck>.md, ready for image/PDF/PPT generation."
---

# Styled Prompts (Content PROMPT → Styled PROMPT)

## Goal

Turn `prompts/content/<deck>.md` into `prompts/styled/<deck>.md` by applying a **style configuration** (e.g. `styles/<style>.toml`) and making concrete design decisions per page:

- infer an appropriate layout *during creation* (no fixed layout catalog required)
- place all content (text, tables, code, figures) so nothing is lost
- specify any required illustrations/diagrams and how they should look
- include consistent typography, spacing, and color constraints

## Inputs

- `prompts/content/<deck>.md`
- `styles/<style>.toml` (treat `[GENERAL].style_prompt` as the source of truth for visual identity)
- Optional: additional references under `references/<style>/` (gitignored)

## Output

Write to: `prompts/styled/<deck>.md`

The output should be compatible with artifact generators (e.g. `scientific-slides`), meaning one block per slide:

- `## Slide N: <title>`
- A short **layout decision** (free-form): what regions exist and why (e.g., “title + left bullets + right diagram”)
- **Content** (fully specified): text, bullet hierarchy, code blocks, table bodies, captions
- **Rendering notes**: what must be drawn as a diagram/figure vs. literal text
- **Style constraints**: apply global style config + any slide-specific overrides
- **Assets**: local image paths to attach, plus how to place them

## Layout inference guidance (during styling)

Choose structure by content, not by an enum:

- Comparison → two-column structure
- Process → flow diagram with numbered steps
- Metrics → chart/table with a one-line takeaway
- Code-heavy → code-first layout with minimal commentary
- Image-heavy → image-first with short caption + key annotation

## Guardrails

- All “Must include” items from the content prompt must appear in the styled prompt.
- If a page is too dense, do not shrink text to illegibility; split into an additional slide.
- Avoid “generic filler visuals”; every figure must convey information.

