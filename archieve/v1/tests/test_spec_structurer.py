import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from slider.spec import parse_markdown_spec
from slider.spec_structurer import structure_material_to_spec_markdown


class TestSpecStructurer(unittest.TestCase):
    def test_structures_headings_into_slides(self) -> None:
        material = """# My Material

This is an intro paragraph that should become a bullet.

## Section One

- First point
- Second point

## Section Two

Paragraph A is long enough to be turned into a bullet. It has a second sentence too.
"""

        spec_md = structure_material_to_spec_markdown(material, max_bullets_per_slide=6)
        deck = parse_markdown_spec(spec_md)
        self.assertEqual(deck.title, "My Material")
        self.assertEqual([s.title for s in deck.slides], ["My Material", "Section One", "Section Two"])
        self.assertTrue(deck.slides[0].bullets)
        self.assertIn("First point", deck.slides[1].bullets)
        self.assertIn("Second point", deck.slides[1].bullets)

    def test_splits_long_material_into_multiple_slides(self) -> None:
        material = """# Title

Para one.

Para two.

Para three.
"""
        spec_md = structure_material_to_spec_markdown(material, max_bullets_per_slide=2)
        deck = parse_markdown_spec(spec_md)
        self.assertEqual(deck.title, "Title")
        self.assertEqual(len(deck.slides), 2)
        self.assertEqual(deck.slides[0].title, "Title")
        self.assertEqual(deck.slides[1].title, "Title (cont.)")
        self.assertEqual(len(deck.slides[0].bullets), 2)
        self.assertEqual(len(deck.slides[1].bullets), 1)

    def test_image_only_lines_do_not_become_bullets(self) -> None:
        material = """# T

## S

![alt](materials/code-agent-huawei/llm-agent.jpg)
"""
        spec_md = structure_material_to_spec_markdown(material, max_bullets_per_slide=6)
        deck = parse_markdown_spec(spec_md)
        self.assertEqual(deck.title, "T")
        self.assertEqual(len(deck.slides), 1)
        self.assertEqual(deck.slides[0].title, "S")
        self.assertEqual(deck.slides[0].bullets, [])
        self.assertEqual(len(deck.slides[0].images), 1)

    def test_preserves_code_blocks_in_spec_markdown(self) -> None:
        material = """# T

## S

```python
print("hello")

print("world")
```
"""
        spec_md = structure_material_to_spec_markdown(material, max_bullets_per_slide=6)
        self.assertIn("```python", spec_md)
        self.assertIn('print("hello")', spec_md)
        self.assertIn("```", spec_md)

    def test_preserves_tables_in_spec_markdown(self) -> None:
        material = """# T

## S

| A | B |
|---|---|
| 1 | 2 |
"""
        spec_md = structure_material_to_spec_markdown(material, max_bullets_per_slide=6)
        self.assertIn("| A | B |", spec_md)
        self.assertIn("|---|---|", spec_md)
        self.assertIn("| 1 | 2 |", spec_md)


if __name__ == "__main__":
    unittest.main()
