#!/usr/bin/env python3
"""
PDF to Images Converter for Presentations

Converts presentation PDFs to images for visual inspection and review.
Supports multiple output formats and resolutions.

Uses PyMuPDF (fitz) as the primary conversion method (no external
system dependencies like poppler required).
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, List

try:
    import fitz  # type: ignore

    HAS_PYMUPDF = True
except Exception:
    HAS_PYMUPDF = False


class PDFToImagesConverter:
    def __init__(
        self,
        pdf_path: str,
        output_prefix: str,
        *,
        dpi: int = 150,
        image_format: str = "jpg",
        first_page: Optional[int] = None,
        last_page: Optional[int] = None,
    ):
        self.pdf_path = Path(pdf_path)
        self.output_prefix = output_prefix
        self.dpi = dpi
        self.image_format = image_format.lower()
        self.first_page = first_page
        self.last_page = last_page

        if self.image_format not in ["jpg", "jpeg", "png"]:
            raise ValueError(f"Unsupported format: {image_format}. Use jpg or png.")

    def convert(self) -> List[Path]:
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")
        if not HAS_PYMUPDF:
            raise RuntimeError("PyMuPDF not installed. Install with: pip install pymupdf")
        return self._convert_with_pymupdf()

    def _convert_with_pymupdf(self) -> List[Path]:
        doc = fitz.open(self.pdf_path)
        start_page = (self.first_page - 1) if self.first_page else 0
        end_page = self.last_page if self.last_page else doc.page_count

        zoom = self.dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        output_files: List[Path] = []
        output_dir = Path(self.output_prefix).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        for page_num in range(start_page, end_page):
            page = doc[page_num]
            pixmap = page.get_pixmap(matrix=matrix)
            output_path = Path(f"{self.output_prefix}-{page_num + 1:03d}.{self.image_format}")
            if self.image_format in ["jpg", "jpeg"]:
                pixmap.save(str(output_path), output="jpeg")
            else:
                pixmap.save(str(output_path), output="png")
            output_files.append(output_path)

        doc.close()
        return output_files


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Convert presentation PDFs to images")
    parser.add_argument("pdf", help="Input PDF")
    parser.add_argument("output_prefix", help="Output prefix (e.g. work/review/slide)")
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--format", default="jpg", dest="image_format")
    parser.add_argument("--first", type=int, dest="first_page")
    parser.add_argument("--last", type=int, dest="last_page")
    args = parser.parse_args(argv)

    converter = PDFToImagesConverter(
        args.pdf,
        args.output_prefix,
        dpi=int(args.dpi),
        image_format=str(args.image_format),
        first_page=args.first_page,
        last_page=args.last_page,
    )
    outputs = converter.convert()
    for p in outputs:
        print(str(p))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

