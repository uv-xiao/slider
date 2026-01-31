# Formatting & consistency protocol (adapted from archived v1)

Condensed from the “formatting consistency protocol” patterns in:

- `archieve/v1/.codex/skills/scientific-slides/SKILL.md`

## Deck-level consistency

Before generating slide images, ensure the styled prompts include:

- a global “formatting goal” (palette, typography feel, background texture, container style)
- repeatable components (badges, callouts, arrows) defined once and reused

## Continuity via previous slide

When generating slide N:

- attach slide N-1’s rendered image to keep visual language consistent
- only skip the previous-slide attachment for deliberate section breaks (explicitly stated)

## Data/figure attachment discipline

If a slide references existing figures/screenshots:

- attach the file(s) to the generator
- describe how to incorporate and annotate them (crop, highlight, labels)

