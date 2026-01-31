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
- **Element spec** (high detail): every element’s type, content, shape, position, and styling
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

## Required detail level (what “Styled PROMPT” means)

The styled prompt must be explicit enough that an image generator can render the slide consistently without guessing.

Use a repeatable element inventory format per slide:

- **Canvas**: 16:9, specify safe margins (e.g., 6–8% on all sides)
- **Grid**: (optional) define a simple grid (e.g., 12-column) or just use percentages
- **Elements**: list every element with a stable id and a bounding box in percentages
  - `id`: e.g. `title`, `subtitle`, `bullets`, `icon_1`, `table_1`, `diagram_1`, `callout_1`
  - `type`: title/text/icon/illustration/diagram/table/code/badge/arrow/shape
  - `bbox`: `x,y,w,h` as percentages of canvas (top-left origin)
  - `z`: layer order (background → content → callouts)
  - `content`: the literal text/table/code, or a precise visual brief for diagrams/illustrations
  - `style`: font weight/size intent, colors, stroke width, corner radius, shadow, padding, alignment

If the style has a “hand-drawn / sketch” theme, explicitly state line weight, wobble, marker highlight behavior, and how to render arrows/containers.

## Adding vivid/intuitive visuals (icons, illustrations, tables)

For each slide, prefer at least one “visual anchor” when it improves comprehension:

- **Icons**: choose a small set (2–4) that reinforces the key points; specify icon style (outline vs solid), stroke width, corner radius, and color usage. Avoid random icon mixing.
- **Illustrations**: describe the scene as a deterministic brief (subjects, pose, props, viewpoint, composition, background treatment). Include the intended emotional tone (friendly/serious) and any constraints (no text inside illustration unless required).
- **Tables**: include full table data, column alignments, header styling, row banding rules, cell padding, and how to highlight key cells (e.g., colored outline or marker underline).
- **Diagrams**: specify nodes and edges explicitly; define shapes (rounded rectangles), arrow types, label placement, and spacing rules.

## Guardrails

- All “Must include” items from the content prompt must appear in the styled prompt.
- If a page is too dense, do not shrink text to illegibility; split into an additional slide.
- Avoid “generic filler visuals”; every figure must convey information.
