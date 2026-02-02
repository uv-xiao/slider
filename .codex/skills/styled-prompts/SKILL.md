---
name: styled-prompts
description: "Convert per-page Content PROMPTs into design-complete Styled PROMPTs using a Markdown style brief, inferring the best layout per page during creation. Outputs prompts/styled/<deck>.md, ready for image/PDF/PPT generation."
---

# Styled Prompts (Content PROMPT → Styled PROMPT)

## Goal

Turn `prompts/content/<deck>.md` into `prompts/styled/<deck>.md` by applying a **style brief** (e.g. `styles/<style>.md`) and making concrete design decisions per page:

- infer an appropriate layout *during creation* (no fixed layout catalog required)
- place all content (text, tables, code, figures) so nothing is lost
- specify any required illustrations/diagrams and how they should look
- include consistent typography, spacing, and color constraints

## Inputs

- `prompts/content/<deck>.md`
- `styles/<style>.md` (treat the style brief content as the source of truth for visual identity)
- Optional: additional references under `references/<style>/` (gitignored)
- Optional: deck preferences under `configs/deck.yaml` (audience/language/style/dimensions)

## Output

Write to: `prompts/styled/<deck>.md`

The output should be compatible with `styled-artifacts`.

**Required deck-level header**: At the top of the file (before the first `## Slide N:`), write a concise **global style/formatting contract** so the renderer has stable “style memory”:

- Formatting goal (background treatment, palette roles, typography feel)
- Reusable components (badges/callouts/arrows/containers) + their visual rules
- Icon/illustration rules (outline vs filled, stroke weight, shading)

Then, one block per slide:

- `## Slide N: <title>`
- A short **layout decision** (free-form): what regions exist and why (e.g., “title + left bullets + right diagram”)
- **Element spec** (high detail): every element’s type, content, shape, position, and styling
- **Rendering notes**: what must be drawn as a diagram/figure vs. literal text
- **Style constraints**: apply global style brief + any slide-specific overrides
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

See templates and pitfalls:
- `references/element-spec-template.md`
- `references/design-guidelines.md`
- `references/layout-patterns.md`
- `references/icon-illustration-guide.md`
- `references/common-pitfalls.md`

## Style system (dimensions + presets)

V2 supports a “dimension” vocabulary (ported from archived v1) to describe style in a reusable way:

- `references/dimensions/presets.md` (preset list)
- `references/dimensions/texture.md`
- `references/dimensions/mood.md`
- `references/dimensions/typography.md`
- `references/dimensions/density.md`

Preset style briefs live in `styles/*.md` (e.g. `styles/blueprint.md`).

Config schema reference (optional):

- `references/config/preferences-schema.md`

## Configuration precedence (recommended)

When both exist:

1. Per-deck: `configs/deck.yaml` (audience/language/style/dimensions)
2. Style file: `styles/<style>.md` (palette/typography/shape language rules; optional Dimensions section)
3. Defaults: conservative, readable, balanced density

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

## Modification & iteration

Treat `prompts/styled/<deck>.md` as the single source of truth.

- **Edit a slide**: modify the slide block, keep the same slide number, and regenerate that slide with `styled-artifacts --only N`.
- **Add a slide**: insert a new `## Slide N:` block, then renumber subsequent slides to keep numbering unique and ordered.
- **Delete a slide**: remove the block, then renumber subsequent slides.
- **Keep the deck-level header** intact: it’s the global style contract applied to all slides.

## Suggested workflow (phases)

1. **Load style brief**
   - Treat the style brief as constraints (palette, typography, shapes), not a fixed layout catalog.
2. **Per-slide design**
   - Choose a structure driven by content (comparison/process/metric/code/image).
   - Produce an explicit element inventory (bbox + z-order + content + style).
   - Add an icon/diagram/table/illustration only when it improves comprehension.
3. **Cross-slide consistency**
   - Ensure repeated elements (badges, icons, callouts) use the same visual language.
   - Ensure spacing and alignment feel consistent across slides.
4. **Legibility & density**
   - If any key text would become small, split the slide instead of shrinking.
5. **Validation mindset**
   - Write prompts so the renderer does not need to guess (explicit geometry and styling).

## Richness targets (what to add beyond text)

Aim for at least one of these per slide when it improves comprehension:

- **Iconography**: small icon per bullet group/category
- **Diagram**: process/architecture/relationship diagrams, explicitly specified
- **Table**: full data table with highlighted cells + one-line insight
- **Illustration**: scene metaphor that encodes meaning (not decoration)

## Review gate (required)

Do not proceed to `styled-artifacts` until the styled prompt passes:

- Every slide has an explicit element inventory (bbox + content + style)
- All “Must include” items from the content prompt are present
- No illegible density (split instead of shrinking)
- Icons/illustrations are consistent and meaningful (not decoration)

## Completion behavior (required)

When this skill is triggered:

1. **Do only this step**: produce/update `prompts/styled/<deck>.md`.
2. **Do not render anything** here (no images/PDF/PPTX, no render sanity-checks). Rendering belongs to `$styled-artifacts`.
3. **End your response with recommended next steps** (options + commands to run next).

Recommended next steps (include this block in your response):

- **Review gate (required before rendering)**: confirm the Styled PROMPT passes the checklist in this skill.
- **Next (render PDF / image-PPTX)**: run `$styled-artifacts`.
  - PDF + image-PPTX:
    - `OPENROUTER_API_KEY=... python3 .codex/skills/styled-artifacts/scripts/styled_prompts_to_artifacts.py --prompts prompts/styled/<deck>.md --workdir artifacts/<deck>/work --pdf artifacts/<deck>/<deck>.pdf --pptx artifacts/<deck>/<deck>.pptx`
  - Sample / partial regeneration:
    - `... --reuse-workdir --only 1-3`
- **Next (editable PPTX)**: invoke `$pptx` and follow the full HTML→PPTX workflow.
  - Minimal dependency commands (local, per-workdir):
    - `cd artifacts/<deck>/work/pptx-html && npm init -y && npm install pptxgenjs playwright sharp && npx playwright install chromium`
  - Visual validation:
    - `python3 .codex/skills/pptx/scripts/thumbnail.py artifacts/<deck>/<deck>.editable.pptx artifacts/<deck>/work/thumbnails --cols 4`
