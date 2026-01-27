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


if __name__ == "__main__":
    unittest.main()
