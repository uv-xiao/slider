import unittest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from slider.styles import get_style, list_style_names


class TestStyles(unittest.TestCase):
    def test_lists_styles(self) -> None:
        names = list_style_names("styles")
        self.assertIn("minimal", names)

    def test_get_style_has_layouts(self) -> None:
        style = get_style("minimal", "styles")
        self.assertTrue(style.general_style_prompt)
        self.assertIn("title_bullets", style.available_layouts())


if __name__ == "__main__":
    unittest.main()
