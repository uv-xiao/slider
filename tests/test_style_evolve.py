import unittest

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from slider.style_evolve import evolve_style_file, list_layout_names_in_style


class TestStyleEvolve(unittest.TestCase):
    def test_evolve_adds_missing_canonical_layouts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            styles_dir = Path(td) / "styles"
            styles_dir.mkdir(parents=True, exist_ok=True)

            (styles_dir / "incomplete.toml").write_text(
                (
                    "[GENERAL]\n"
                    'default_layout = "title_only"\n'
                    'style_prompt = """\nTest prompt.\n"""\n'
                    "\n"
                    "[layouts.title_only]\n"
                    'layout_description = """\nTitle only.\n"""\n'
                    'style_prompt = """\nUse the global style.\n"""\n'
                ),
                "utf-8",
            )

            out_path = styles_dir / "out.toml"
            result = evolve_style_file(
                style_path=styles_dir / "incomplete.toml",
                styles_dir=styles_dir,
                target="canonical",
                out_path=out_path,
            )
            self.assertEqual(
                result.added_layouts,
                (
                    "image_full_bleed_caption",
                    "image_left_text_right",
                    "title_bullets",
                    "title_bullets_code",
                    "title_bullets_table",
                    "title_code",
                    "title_table",
                    "two_column_bullets",
                ),
            )

            layouts = list_layout_names_in_style(out_path)
            self.assertIn("title_only", layouts)
            self.assertIn("title_bullets", layouts)
            self.assertIn("title_code", layouts)
            self.assertIn("title_bullets_code", layouts)
            self.assertIn("title_table", layouts)
            self.assertIn("title_bullets_table", layouts)
            self.assertIn("two_column_bullets", layouts)
            self.assertIn("image_left_text_right", layouts)
            self.assertIn("image_full_bleed_caption", layouts)

            # Idempotent: evolving again should add nothing.
            second = evolve_style_file(style_path=out_path, styles_dir=styles_dir, target="canonical")
            self.assertEqual(second.added_layouts, tuple())


if __name__ == "__main__":
    unittest.main()
