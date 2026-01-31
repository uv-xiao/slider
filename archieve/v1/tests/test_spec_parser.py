import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from slider.spec import infer_layout, parse_markdown_spec


class TestSpecParser(unittest.TestCase):
    def test_parses_h1_and_h2(self) -> None:
        deck = parse_markdown_spec("# Title\n\n## Slide A\n- one\n- two\n")
        self.assertEqual(deck.title, "Title")
        self.assertEqual(len(deck.slides), 1)
        self.assertEqual(deck.slides[0].title, "Slide A")
        self.assertEqual(deck.slides[0].bullets, ["one", "two"])

    def test_infers_layouts(self) -> None:
        deck = parse_markdown_spec("# T\n\n## S\n- a\n")
        self.assertEqual(infer_layout(deck.slides[0]), "title_bullets")

        deck2 = parse_markdown_spec("# T\n\n## S\n" + "\n".join([f"- {i}" for i in range(7)]) + "\n")
        self.assertEqual(infer_layout(deck2.slides[0]), "two_column_bullets")

        deck3 = parse_markdown_spec("# T\n\n## S\n![alt](x.png)\n")
        self.assertEqual(infer_layout(deck3.slides[0]), "image_left_text_right")

        deck4 = parse_markdown_spec("# T\n\n## S\n```text\nhi\n```\n")
        self.assertEqual(infer_layout(deck4.slides[0]), "title_code")

        deck5 = parse_markdown_spec("# T\n\n## S\n- a\n```text\nhi\n```\n")
        self.assertEqual(infer_layout(deck5.slides[0]), "title_bullets_code")

        deck6 = parse_markdown_spec("# T\n\n## S\n| A | B |\n|---|---|\n| 1 | 2 |\n")
        self.assertEqual(infer_layout(deck6.slides[0]), "title_table")

    def test_does_not_parse_bullets_inside_code_fences(self) -> None:
        deck = parse_markdown_spec("# T\n\n## S\n```text\n- not a bullet\n```\n- real bullet\n")
        self.assertEqual(deck.title, "T")
        self.assertEqual(len(deck.slides), 1)
        self.assertEqual(deck.slides[0].bullets, ["real bullet"])
        self.assertIn("```text", deck.slides[0].body)
        self.assertIn("- not a bullet", deck.slides[0].body)


if __name__ == "__main__":
    unittest.main()
