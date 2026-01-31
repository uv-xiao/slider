#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests", file=sys.stderr)
    raise SystemExit(1)


def _image_to_data_url(path: Path) -> str:
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    mime = "image/png"
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif path.suffix.lower() == ".webp":
        mime = "image/webp"
    return f"data:{mime};base64,{b64}"


def _find_data_url(value: Any) -> Optional[str]:
    if isinstance(value, str):
        if value.startswith("data:image/") and ";base64," in value:
            return value
        return None
    if isinstance(value, dict):
        for v in value.values():
            found = _find_data_url(v)
            if found:
                return found
        return None
    if isinstance(value, list):
        for v in value:
            found = _find_data_url(v)
            if found:
                return found
        return None
    return None


def _decode_data_url(data_url: str) -> Optional[bytes]:
    m = re.match(r"^data:image/[^;]+;base64,(.+)$", data_url)
    if not m:
        return None
    try:
        return base64.b64decode(m.group(1))
    except Exception:
        return None


class SlideImageGenerator:
    """
    V2 generator: single-pass image generation (no automated review/regenerate loop).

    Review is expected to happen on prompts (content/styled) before artifact generation.
    """

    def __init__(self, api_key: str, *, verbose: bool = False):
        self.api_key = api_key
        self.verbose = verbose
        self.base_url = "https://openrouter.ai/api/v1"
        self.image_model = "google/gemini-3-pro-image-preview"

    def _request(self, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=300)
        if resp.status_code >= 400:
            raise RuntimeError(f"OpenRouter HTTP {resp.status_code}: {resp.text[:800]}")
        return resp.json()

    def generate(self, *, prompt: str, attachments: list[Path]) -> bytes:
        if attachments:
            content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
            for p in attachments:
                content.append({"type": "image_url", "image_url": {"url": _image_to_data_url(p)}})
            message: Any = {"role": "user", "content": content}
        else:
            message = {"role": "user", "content": prompt}

        payload: dict[str, Any] = {
            "model": self.image_model,
            "messages": [message],
            "modalities": ["image", "text"],
        }
        data = self._request(payload)

        if "error" in data:
            raise RuntimeError(str(data["error"]))

        url = _find_data_url(data)
        if not url:
            raise RuntimeError("No image data URL found in response.")
        img = _decode_data_url(url)
        if not img:
            raise RuntimeError("Failed to decode base64 image from response.")
        return img


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a slide image from a detailed prompt (single-pass)")
    parser.add_argument("prompt", help="Slide prompt text")
    parser.add_argument("-o", "--output", required=True, help="Output image path")
    parser.add_argument("--attach", action="append", dest="attachments", metavar="FILE", help="Attach image file(s)")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
        return 2

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    attachments: list[Path] = []
    if args.attachments:
        for a in args.attachments:
            p = Path(a)
            if not p.exists():
                print(f"Error: attachment not found: {p}", file=sys.stderr)
                return 2
            attachments.append(p)

    gen = SlideImageGenerator(api_key=api_key, verbose=bool(args.verbose))
    img = gen.generate(prompt=args.prompt, attachments=attachments)
    output_path.write_bytes(img)
    if args.verbose:
        print(f"Wrote {output_path} ({output_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

