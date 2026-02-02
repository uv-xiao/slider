from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayoutCatalogEntry:
    name: str
    layout_description: str
    style_prompt: str


CANONICAL_LAYOUTS: dict[str, LayoutCatalogEntry] = {
    "title_only": LayoutCatalogEntry(
        name="title_only",
        layout_description="Title-only slide with generous whitespace. Use for section breaks or chapter titles.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Place a large title (and optional subtitle) with ample whitespace.\n"
            "- Keep the slide intentionally sparse; no body copy unless explicitly provided.\n"
            "\n"
            "Styling:\n"
            "- Match the typography, line weights, colors, and decorative motifs used in other layouts of this style.\n"
        ),
    ),
    "title_bullets": LayoutCatalogEntry(
        name="title_bullets",
        layout_description="Title + 1–6 bullets. Use for standard content slides.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Title at top (optionally bilingual if the style uses bilingual headings).\n"
            "- Bullet list beneath, 1–6 bullets, comfortable line spacing.\n"
            "- If a short 'body' paragraph is present, place it above the bullets or as the last bullet.\n"
            "\n"
            "Styling:\n"
            "- Use the same bullet iconography, section boxes, and accent colors as the rest of the style.\n"
            "- Maintain consistent margins and alignment.\n"
        ),
    ),
    "two_column_bullets": LayoutCatalogEntry(
        name="two_column_bullets",
        layout_description="Title + bullets split into 2 columns (for bullet-heavy slides).",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Title at top.\n"
            "- Split bullets into two balanced columns below the title.\n"
            "- Keep columns aligned to a consistent baseline and avoid cramped text.\n"
            "\n"
            "Styling:\n"
            "- Use subtle guides (dividers, containers, or spacing) consistent with the style.\n"
            "- Ensure both columns feel equally weighted.\n"
        ),
    ),
    "image_left_text_right": LayoutCatalogEntry(
        name="image_left_text_right",
        layout_description="Image on the left, text (bullets/body) on the right.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Left: one primary image (optionally with a short caption if provided).\n"
            "- Right: title and supporting text (bullets and/or short body lines).\n"
            "- Keep the image visually prominent; do not let text overpower it.\n"
            "\n"
            "Styling:\n"
            "- Use frames, outlines, stickers, or containers consistent with the style.\n"
            "- Maintain strong contrast for any captions or overlays.\n"
        ),
    ),
    "image_full_bleed_caption": LayoutCatalogEntry(
        name="image_full_bleed_caption",
        layout_description="Full-bleed image with a short caption.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Use a single image as the background (full-bleed / edge-to-edge).\n"
            "- Place a short caption (and optional title) in a safe area.\n"
            "\n"
            "Styling:\n"
            "- Ensure text remains readable using consistent style techniques (overlay, label, outline, or container).\n"
            "- Avoid covering key parts of the image.\n"
        ),
    ),
    "title_code": LayoutCatalogEntry(
        name="title_code",
        layout_description="Title + code block. Use when the slide contains a fenced code block and little/no bullets.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Title at top.\n"
            "- Render the code block in a dedicated code container (monospace, high contrast).\n"
            "- Preserve code formatting exactly; avoid reflowing or paraphrasing.\n"
            "\n"
            "Styling:\n"
            "- Use a hand-drawn container/outline consistent with the style.\n"
            "- Keep the code readable (sufficient font size, line spacing).\n"
        ),
    ),
    "title_bullets_code": LayoutCatalogEntry(
        name="title_bullets_code",
        layout_description="Title + short bullets + code block. Use when the slide has both bullets and a fenced code block.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Title at top.\n"
            "- 2–4 bullets to frame the idea.\n"
            "- Code block in a code container below or to the side.\n"
            "- Preserve code formatting exactly.\n"
            "\n"
            "Styling:\n"
            "- Keep a clear hierarchy: bullets explain, code demonstrates.\n"
        ),
    ),
    "title_table": LayoutCatalogEntry(
        name="title_table",
        layout_description="Title + table. Use when the slide contains a Markdown table and little/no bullets.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Title at top.\n"
            "- Render the table clearly with visible grid lines and readable text.\n"
            "\n"
            "Styling:\n"
            "- Header row may use a light tinted fill consistent with the style accent colors.\n"
            "- Keep spacing generous; avoid cramped cells.\n"
        ),
    ),
    "title_bullets_table": LayoutCatalogEntry(
        name="title_bullets_table",
        layout_description="Title + short bullets + table. Use when the slide has both bullets and a Markdown table.",
        style_prompt=(
            "Follow the [GENERAL].style_prompt global constraints.\n"
            "\n"
            "Structure:\n"
            "- Title at top.\n"
            "- 1–3 bullets summarizing the point.\n"
            "- Table as the main visual evidence.\n"
            "\n"
            "Styling:\n"
            "- Make the table the visual focus; bullets should stay short.\n"
        ),
    ),
}
