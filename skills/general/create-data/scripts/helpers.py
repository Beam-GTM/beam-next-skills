"""Shared helpers for export scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> list[dict[str, Any]]:
    """Load a generated JSON dataset file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def truncate(text: str, max_len: int = 120) -> str:
    """Truncate text with ellipsis if it exceeds max_len."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def style_header(name: str, style: str) -> str:
    """Apply a casing style to a column header name."""
    if style == "Title Case":
        return name.replace("_", " ").title()
    if style == "UPPER":
        return name.replace("_", " ").upper()
    return name
