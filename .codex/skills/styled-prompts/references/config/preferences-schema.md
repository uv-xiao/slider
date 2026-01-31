# Deck preference schema (ported from archived v1)

This schema is ported from archived v1 to standardize v2 deck preferences.

Recommended v2 location: `configs/deck.yaml`

## Full Schema

```yaml
# Slide Deck Preferences

## Defaults
style: blueprint              # Preset name OR "custom"
audience: general             # beginners | intermediate | experts | executives | general
language: auto                # auto | en | zh | ja | etc.
review: true                  # true = review prompts (content/styled) before rendering artifacts

## Custom Dimensions (only when style: custom)
dimensions:
  texture: clean              # clean | grid | organic | pixel | paper
  mood: professional          # professional | warm | cool | vibrant | dark | neutral
  typography: geometric       # geometric | humanist | handwritten | editorial | technical
  density: balanced           # minimal | balanced | dense

## Custom Styles (optional)
custom_styles:
  my-style:
    texture: organic
    mood: warm
    typography: humanist
    density: minimal
    description: "My custom warm and friendly style"
```

## Field Descriptions

### Defaults

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `style` | string | `blueprint` | Preset name, `custom`, or custom style name |
| `audience` | string | `general` | Default target audience |
| `language` | string | `auto` | Output language (auto = detect from input) |
| `review` | boolean | `true` | Show outline review before generation |

### Custom Dimensions

Only used when `style: custom`. Defines dimension values directly.

| Field | Options | Default |
|-------|---------|---------|
| `texture` | clean, grid, organic, pixel, paper | clean |
| `mood` | professional, warm, cool, vibrant, dark, neutral | professional |
| `typography` | geometric, humanist, handwritten, editorial, technical | geometric |
| `density` | minimal, balanced, dense | balanced |

### Custom Styles

Define reusable custom dimension combinations.

```yaml
custom_styles:
  style-name:
    texture: <texture>
    mood: <mood>
    typography: <typography>
    density: <density>
    description: "Optional description"
```

Then use with v2 by setting `style: style-name` in `configs/deck.yaml`. For reproducibility, also keep a matching style brief in `styles/style-name.md`.

## Minimal Examples

### Just change default style

```yaml
style: sketch-notes
```

This corresponds to a style brief at `styles/sketch-notes.md`.

### Prefer no reviews

```yaml
review: false
```

### Custom default dimensions

```yaml
style: custom
dimensions:
  texture: organic
  mood: professional
  typography: humanist
  density: minimal
```

### Define reusable custom style

```yaml
custom_styles:
  brand-style:
    texture: clean
    mood: vibrant
    typography: editorial
    density: balanced
    description: "Company brand style"
```

## Location

Recommended v2 location: `configs/deck.yaml` (project).
