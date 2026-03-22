#!/usr/bin/env python3
"""Google Gemini Image — generate, edit, and refine images (Gemini 3.1 Flash Image)."""

import argparse
import os
import sys
from io import BytesIO
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

for parent in Path(__file__).resolve().parents:
    env_file = parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())
        break

from google import genai
from google.genai import types
from PIL import Image

from gemini_client import generate_filename, get_output_dir

MODEL_IMAGE = "gemini-3.1-flash-image-preview"

ASPECT_RATIOS = (
    "1:1",
    "1:4",
    "1:8",
    "2:3",
    "3:2",
    "3:4",
    "4:1",
    "4:3",
    "4:5",
    "5:4",
    "8:1",
    "9:16",
    "16:9",
    "21:9",
)
IMAGE_SIZES = ("512", "1K", "2K", "4K")


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(
            "ERROR: GEMINI_API_KEY not set\nGet your key from: https://aistudio.google.com/app/apikey",
            file=sys.stderr,
        )
        sys.exit(1)
    return genai.Client(api_key=api_key)


def _iter_response_parts(response):
    if getattr(response, "candidates", None) and response.candidates:
        c0 = response.candidates[0]
        if getattr(c0, "content", None) and c0.content.parts:
            return list(c0.content.parts)
    if getattr(response, "parts", None):
        return list(response.parts)
    return []


def save_image(response, prefix: str, output_path: str | None = None) -> Path:
    parts = _iter_response_parts(response)
    for part in parts:
        image = None
        if getattr(part, "inline_data", None) is not None and part.inline_data.data:
            image = Image.open(BytesIO(part.inline_data.data))
        elif hasattr(part, "as_image") and callable(part.as_image):
            try:
                image = part.as_image()
            except Exception:
                image = None
        if image is None:
            continue

        if output_path:
            save_path = Path(output_path)
            if not save_path.is_absolute():
                save_path = get_output_dir() / save_path
        else:
            save_path = get_output_dir() / generate_filename(prefix)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(save_path, "PNG")
        print(f"Image saved to: {save_path}")
        return save_path

    print("ERROR: No image in response", file=sys.stderr)
    for part in parts:
        if hasattr(part, "text") and part.text:
            print(f"Response: {part.text}", file=sys.stderr)
    sys.exit(1)


def handle_error(e):
    msg = str(e).upper()
    if "SAFETY" in msg:
        print("ERROR: Content blocked by safety filter", file=sys.stderr)
    elif "RATE" in msg or "QUOTA" in msg:
        print("ERROR: Rate limit exceeded — wait and retry", file=sys.stderr)
    elif "API_KEY" in msg or "AUTHENTICATION" in msg:
        print("ERROR: Invalid API key — check GEMINI_API_KEY", file=sys.stderr)
    else:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)


def load_pil_image(path_str: str) -> Image.Image:
    p = Path(path_str)
    if not p.exists():
        print(f"ERROR: Image not found: {path_str}", file=sys.stderr)
        sys.exit(1)
    return Image.open(p)


def get_last_image() -> Path | None:
    images = list(get_output_dir().glob("*.png"))
    return max(images, key=lambda x: x.stat().st_mtime) if images else None


def _image_config(aspect: str, size: str) -> types.ImageConfig:
    return types.ImageConfig(aspect_ratio=aspect, image_size=size)


def _gen_config(aspect: str, size: str) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=_image_config(aspect, size),
    )


# ── Actions ──────────────────────────────────────────────────────────────────


def do_generate(args):
    client = get_client()
    print(f'Generating: "{args.prompt}"')
    cfg = _gen_config(args.aspect, args.size)
    try:
        response = client.models.generate_content(
            model=MODEL_IMAGE,
            contents=[args.prompt],
            config=cfg,
        )
        save_image(response, "generated", args.output)
    except Exception as e:
        handle_error(e)


def do_edit(args):
    client = get_client()
    img = load_pil_image(args.image)
    print(f'Editing {args.image}: "{args.prompt}"')
    cfg = _gen_config(args.aspect, args.size)
    try:
        response = client.models.generate_content(
            model=MODEL_IMAGE,
            contents=[f"Edit this image: {args.prompt}", img],
            config=cfg,
        )
        save_image(response, "edited", args.output)
    except Exception as e:
        handle_error(e)


def do_refine(args):
    client = get_client()
    if args.image:
        img = load_pil_image(args.image)
        name = args.image
    else:
        last = get_last_image()
        if not last:
            print(
                "ERROR: No previous image to refine. Generate one first or use --image.",
                file=sys.stderr,
            )
            sys.exit(1)
        img = load_pil_image(str(last))
        name = str(last)
    print(f'Refining {name}: "{args.prompt}"')
    cfg = _gen_config(args.aspect, args.size)
    try:
        response = client.models.generate_content(
            model=MODEL_IMAGE,
            contents=[f"Refine this image: {args.prompt}", img],
            config=cfg,
        )
        save_image(response, "refined", args.output)
    except Exception as e:
        handle_error(e)


def main():
    parser = argparse.ArgumentParser(description="Google Gemini Image — generate, edit, refine")
    sub = parser.add_subparsers(dest="action", required=True)

    gen = sub.add_parser("generate", help="Generate image from text")
    gen.add_argument("prompt", help="Text prompt")
    gen.add_argument("--aspect", choices=ASPECT_RATIOS, default="1:1")
    gen.add_argument("--size", choices=IMAGE_SIZES, default="1K", help="Output resolution (Gemini 3.1)")
    gen.add_argument("-o", "--output", help="Output filename")

    edit = sub.add_parser("edit", help="Edit an existing image")
    edit.add_argument("image", help="Input image path")
    edit.add_argument("prompt", help="Edit instructions")
    edit.add_argument("--aspect", choices=ASPECT_RATIOS, default="1:1")
    edit.add_argument("--size", choices=IMAGE_SIZES, default="1K")
    edit.add_argument("-o", "--output", help="Output filename")

    ref = sub.add_parser("refine", help="Refine last image or specified image")
    ref.add_argument("prompt", help="Refinement instructions")
    ref.add_argument("-i", "--image", help="Image to refine (default: last generated)")
    ref.add_argument("--aspect", choices=ASPECT_RATIOS, default="1:1")
    ref.add_argument("--size", choices=IMAGE_SIZES, default="1K")
    ref.add_argument("-o", "--output", help="Output filename")

    args = parser.parse_args()
    {"generate": do_generate, "edit": do_edit, "refine": do_refine}[args.action](args)


if __name__ == "__main__":
    main()
