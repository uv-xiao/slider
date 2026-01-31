# Element spec template (v2 Styled PROMPT)

Use a repeatable inventory so the renderer does not guess.

## Deck-level style contract (required)

At the very top of `prompts/styled/<deck>.md` (before the first `## Slide N:`), include a short global block describing:

- formatting goal (background treatment, palette roles, typography feel)
- reusable component language (badges/callouts/arrows/containers)
- icon/illustration rules (outline vs filled, stroke weight, shading)

This is the primary “style memory” that is applied to every slide, and complements the previous-slide attachment used during rendering.

## Canvas

- Aspect: 16:9
- Safe margin: 6–8% (unless full-bleed is required)

## Elements (example schema)

For each element:

- `id`: stable identifier
- `type`: title | text | bullets | icon | illustration | diagram | table | code | badge | arrow | shape
- `bbox`: `x,y,w,h` as percentages of canvas (top-left origin)
- `z`: background → content → callout
- `content`: literal text/table/code, or deterministic diagram/illustration brief
- `style`: colors, stroke width, corner radius, padding, font intent, alignment

## Example

- `id`: `table_1`
- `type`: `table`
- `bbox`: `8,34,84,44`
- `z`: `content`
- `content`: full table (rows/cols)
- `style`: header fill, row banding, highlighted cells, padding, border weight
