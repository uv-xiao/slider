# Element spec template (v2 Styled PROMPT)

Use a repeatable inventory so the renderer does not guess.

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

