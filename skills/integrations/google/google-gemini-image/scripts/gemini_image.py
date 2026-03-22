#!/usr/bin/env python3
"""Google Gemini Image — generate, edit, and refine images."""

import argparse
import os
import sys
from pathlib import Path
from io import BytesIO

scripts_dir = Path(__file__).resolve().parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

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

from gemini_client import get_output_dir, generate_filename

MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set\nGet your key from: https://aistudio.google.com/app/apikey", file=sys.stderr)
        sys.exit(1)
    return genai.Client(api_key=api_key)


def save_image(response, prefix: str, output_path: str = None) -> Path:
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
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
    for part in response.candidates[0].content.parts:
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


def load_image(path_str: str):
    p = Path(path_str)
    if not p.exists():
        print(f"ERROR: Image not found: {path_str}", file=sys.stderr)
        sys.exit(1)
    with open(p, "rb") as f:
        data = f.read()
    mime = MIME_TYPES.get(p.suffix.lower(), "image/png")
    return data, mime, p.name


def get_last_image() -> Path | None:
    images = list(get_output_dir().glob("*.png"))
    return max(images, key=lambda x: x.stat().st_mtime) if images else None


# ── Actions ──────────────────────────────────────────────────────────────────

def do_generate(args):
    client = get_client()
    print(f'Generating: "{args.prompt}"')
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=args.prompt,
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )
        save_image(response, "generated", args.output)
    except Exception as e:
        handle_error(e)


def do_edit(args):
    client = get_client()
    image_data, mime, name = load_image(args.image)
    print(f'Editing {name}: "{args.prompt}"')
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[types.Content(parts=[
                types.Part(inline_data=types.Blob(mime_type=mime, data=image_data)),
                types.Part(text=f"Edit this image: {args.prompt}"),
            ])],
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )
        save_image(response, "edited", args.output)
    except Exception as e:
        handle_error(e)


def do_refine(args):
    client = get_client()
    if args.image:
        image_data, mime, name = load_image(args.image)
    else:
        last = get_last_image()
        if not last:
            print("ERROR: No previous image to refine. Generate one first or use --image.", file=sys.stderr)
            sys.exit(1)
        image_data, mime, name = load_image(str(last))
    print(f'Refining {name}: "{args.prompt}"')
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[types.Content(parts=[
                types.Part(inline_data=types.Blob(mime_type=mime, data=image_data)),
                types.Part(text=f"Refine this image: {args.prompt}"),
            ])],
            config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
        )
        save_image(response, "refined", args.output)
    except Exception as e:
        handle_error(e)


def main():
    parser = argparse.ArgumentParser(description="Google Gemini Image — generate, edit, refine")
    sub = parser.add_subparsers(dest="action", required=True)

    gen = sub.add_parser("generate", help="Generate image from text")
    gen.add_argument("prompt", help="Text prompt")
    gen.add_argument("--aspect", choices=["1:1", "4:3", "16:9", "9:16"], default="1:1")
    gen.add_argument("-o", "--output", help="Output filename")

    edit = sub.add_parser("edit", help="Edit an existing image")
    edit.add_argument("image", help="Input image path")
    edit.add_argument("prompt", help="Edit instructions")
    edit.add_argument("-o", "--output", help="Output filename")

    ref = sub.add_parser("refine", help="Refine last image or specified image")
    ref.add_argument("prompt", help="Refinement instructions")
    ref.add_argument("-i", "--image", help="Image to refine (default: last generated)")
    ref.add_argument("-o", "--output", help="Output filename")

    args = parser.parse_args()
    {"generate": do_generate, "edit": do_edit, "refine": do_refine}[args.action](args)


if __name__ == "__main__":
    main()
