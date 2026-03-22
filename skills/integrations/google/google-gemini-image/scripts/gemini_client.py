"""Shared helpers for Gemini image scripts (output paths)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def find_beam_next_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "CLAUDE.md").exists():
            return parent
    return Path.cwd()


def get_output_dir() -> Path:
    out = find_beam_next_root() / "04-workspace" / "generated-images"
    out.mkdir(parents=True, exist_ok=True)
    return out


def generate_filename(prefix: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.png"
