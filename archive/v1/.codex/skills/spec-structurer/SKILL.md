---
name: spec-structurer
description: "Convert unstructured Markdown material/notes into a structured multi-slide SPEC (specs/*.md) by analyzing headings, bullets, and paragraphs, then dividing content into per-slide sections. Use when asked to 'turn notes into a SPEC', 'split this markdown into slides/pages', 'structure unstructured material into specs/<deck>.md', or 'organize content into per-page slide format'."
---

# Spec Structurer

Convert an unstructured Markdown document (notes, outline, pasted content) into a structured slider SPEC Markdown with `# <Deck Title>` and `## <Slide Title>` sections.

## Quick start

- Convert a file into a SPEC:
  - `PYTHONPATH=src python3 -m slider structure-spec --material materials/notes.md --out specs/mydeck.md`
  - Or via Pixi: `pixi run structure-spec --material materials/notes.md --out specs/mydeck.md`

- Convert from stdin (paste content):
  - `cat notes.md | PYTHONPATH=src python3 -m slider structure-spec --material - --out specs/mydeck.md`

## Required: Review & Align (do not skip)

Auto-structuring is only a first draft. Always re-audit the generated SPEC against the original material and fix misalignment.

Workflow:

1. Generate a draft SPEC (prefer smaller pages):
   - `pixi run structure-spec --material materials/<deck>/README.md --out specs/<deck>.auto.md --max-bullets 6`
2. Create the reviewed SPEC:
   - Copy `specs/<deck>.auto.md` to `specs/<deck>.md`, then edit `specs/<deck>.md` by comparing with `materials/<deck>/README.md`.

Alignment checklist (material → SPEC):

- **Coverage**: Each major `##` section in the material maps to 1–2 slides in the SPEC (not 6–10).
- **Order**: Slide order matches the narrative order in the material.
- **No “meta bullets”**: Remove bullets like “示意图：” / “约束：” / “参考：” unless you truly want them on slides.
- **Bullet quality**: Prefer 3–5 bullets per slide, each short enough to be spoken (avoid long paragraphs).
- **English terms**: Keep technical terms in English exactly as written in the material.
- **Tone**: If the audience is seniors, keep a learning/exchange tone（后辈姿态）, avoid “指教式”措辞.
- **Images**: Ensure image-only lines don’t become text bullets; if you include images, add a brief caption bullet when needed.
- **Preserve Markdown blocks**: Keep code fences and tables as Markdown blocks in the SPEC (do not flatten them into bullets).

If the result still feels too dense:

- Split one material section into 2 slides with clearer titles.
- Rewrite bullets to be shorter (keep meaning, keep English terms), and drop low-priority details into the material (not the SPEC).

## Rule: No Information Deletion During Review

Once the material has been finalized, the review stage must not delete information. Only re-page and reorganize content.

Allowed during review:
- Split a dense slide into multiple slides (preferred).
- Move bullets/paragraphs/blocks between slides.
- Re-title slides for clarity.
- Reformat without loss (e.g., break a long bullet into multiple bullets, but keep all text).

Not allowed during review:
- Dropping bullets/paragraphs/code/table rows because they “feel too detailed”.
- Replacing content with summaries that remove facts.

## Common options

- Override the deck title:
  - `PYTHONPATH=src python3 -m slider structure-spec --material materials/notes.md --out specs/mydeck.md --title "My Deck"`

- Control slide splitting (max bullets per slide):
  - `PYTHONPATH=src python3 -m slider structure-spec --material materials/notes.md --out specs/mydeck.md --max-bullets 6`

## Workflow tips

- If the material has clear sections, add/clean up `##` headings first; they become slide boundaries.
- Keep each section to ~3–6 bullets for best downstream prompt rendering.
- After structuring, refine the SPEC manually (rename slide titles, prune bullets), then run `slider render-prompts`.
