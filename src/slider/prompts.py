from __future__ import annotations

from pathlib import Path

from .spec import Deck, infer_layout
from .styles import Layout, Style


def _read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def _choose_layout(style: Style, inferred: str) -> tuple[str, Layout]:
    if inferred in style.layouts:
        return inferred, style.layouts[inferred]

    if style.default_layout and style.default_layout in style.layouts:
        return style.default_layout, style.layouts[style.default_layout]

    if "title_bullets" in style.layouts:
        return "title_bullets", style.layouts["title_bullets"]

    available = style.available_layouts()
    if not available:
        raise ValueError(f"Style '{style.name}' has no layouts defined")
    chosen = available[0]
    return chosen, style.layouts[chosen]


def render_deck_prompts(
    deck: Deck,
    style: Style,
    workflow_prompt_path: str | Path = "prompts/workflow-prompt.md",
) -> str:
    workflow = _read_optional(Path(workflow_prompt_path))

    out: list[str] = []
    if workflow:
        out.append("# Workflow Prompt\n")
        out.append(workflow)
        out.append("")

    out.append(f"# Deck: {deck.title}")
    out.append(f"Style: {style.name}")
    out.append("")

    if style.general_style_prompt.strip():
        out.append("## Style: general prompt")
        out.append(style.general_style_prompt.strip())
        out.append("")

    out.append("## Style: layouts")
    for layout_name in style.available_layouts():
        layout = style.layouts[layout_name]
        desc = layout.layout_description.strip() or "(no description)"
        out.append(f"- {layout_name}: {desc}")
    out.append("")

    for i, slide in enumerate(deck.slides, start=1):
        inferred = infer_layout(slide)
        chosen_name, chosen = _choose_layout(style, inferred)

        out.append(f"## Slide {i}: {slide.title}")
        if chosen_name == inferred:
            out.append(f"Layout: {chosen_name}")
        else:
            out.append(f"Layout: {chosen_name} (inferred: {inferred})")
        out.append("")

        if chosen.layout_description.strip():
            out.append("Layout description:")
            out.append(chosen.layout_description.strip())
            out.append("")

        if chosen.style_prompt.strip():
            out.append("Layout prompt:")
            out.append(chosen.style_prompt.strip())
            out.append("")

        if slide.bullets:
            out.append("Content (bullets):")
            for b in slide.bullets:
                out.append(f"- {b}")
            out.append("")

        if slide.body:
            out.append("Content (body):")
            for line in slide.body:
                out.append(f"- {line}")
            out.append("")

        if slide.images:
            out.append("Images:")
            for img in slide.images:
                alt = img.alt or "(no alt)"
                out.append(f"- alt: {alt} | src: {img.src}")
            out.append("")

    return "\n".join(out).rstrip() + "\n"

