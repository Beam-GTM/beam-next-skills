---
name: google-gemini-image
type: skill
version: '2.0'
description: Generate, edit, and refine images with Google Gemini. Load when user says
  'generate image', 'edit image', 'refine image', 'text to image', 'gemini image',
  'modify image'.
category: integrations
tags:
- google
- gemini
- images
platform: Google Gemini
updated: '2026-03-23'
visibility: public
---
# Google Gemini Image

Unified skill for text-to-image generation, image editing, and iterative refinement.

Replaces: `gemini-generate-image`, `gemini-edit-image`, `gemini-refine-image`.

## Usage

```bash
# Generate from text prompt
uv run python scripts/gemini_image.py generate "a cat in space"
uv run python scripts/gemini_image.py generate "sunset over mountains" --aspect 16:9
uv run python scripts/gemini_image.py generate "abstract art" --output my_art.png

# Edit an existing image
uv run python scripts/gemini_image.py edit photo.png "make the sky blue"
uv run python scripts/gemini_image.py edit scene.jpg "add clouds" --output result.png

# Refine the last generated/edited image
uv run python scripts/gemini_image.py refine "add more stars"
uv run python scripts/gemini_image.py refine "make it brighter" --image specific.png
```

## Models

| Action | Model | Input |
|--------|-------|-------|
| generate | `gemini-2.0-flash-exp-image-generation` | Text prompt only |
| edit | `gemini-2.0-flash-exp` | Image + text instructions |
| refine | `gemini-2.0-flash-exp` | Image (or last output) + text instructions |

## Requirements

- `GEMINI_API_KEY` in `.env` (get from https://aistudio.google.com/app/apikey)
- `pip install google-genai Pillow`

## Output

Images save as PNG to `04-workspace/generated-images/` (or `--output` path).
Filenames auto-generated with timestamp: `generated_20260323_143000.png`, `edited_...`, `refined_...`.
