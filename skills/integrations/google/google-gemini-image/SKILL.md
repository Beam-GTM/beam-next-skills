---
name: google-gemini-image
type: skill
version: '2.1'
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
uv run python scripts/gemini_image.py generate "sunset over mountains" --aspect 16:9 --size 2K
uv run python scripts/gemini_image.py generate "abstract art" --output my_art.png

# Edit an existing image
uv run python scripts/gemini_image.py edit photo.png "make the sky blue"
uv run python scripts/gemini_image.py edit scene.jpg "add clouds" --aspect 4:3 --size 1K --output result.png

# Refine the last generated/edited image
uv run python scripts/gemini_image.py refine "add more stars"
uv run python scripts/gemini_image.py refine "make it brighter" --image specific.png
```

## Model

All actions use **`gemini-3.1-flash-image-preview`** (Nano Banana 2). Inputs are text-only, or image + text for edit/refine.

Legacy `gemini-2.0-flash-exp*` models are deprecated; Google scheduled shutdown **June 1, 2026** — this skill targets 3.1 only.

## Aspect ratio and size

- **`--aspect`**: `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9` (default `1:1`).
- **`--size`**: `512`, `1K`, `2K`, `4K` (default `1K`). Passed to the API as `image_config.image_size`.

## Requirements

- `GEMINI_API_KEY` in `.env` (get from https://aistudio.google.com/app/apikey)
- `pip install google-genai Pillow`

## Output

Images save as PNG to `04-workspace/generated-images/` (or `--output` path).
Filenames auto-generated with timestamp: `generated_20260323_143000.png`, `edited_...`, `refined_...`.

Shared path helpers live in `scripts/gemini_client.py`.
