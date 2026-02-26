"""CSV export with randomized formatting variations.

Variations per export:
- Delimiter: comma, semicolon, tab, pipe
- Header style: snake_case, Title Case, UPPER
- Column ordering: shuffled randomly
- Metadata: flattened into columns vs single JSON blob column
- Quoting: QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONNUMERIC
- Optional: transformation_rules column, headers row
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from typing import Any

from helpers import style_header

_DELIMITERS = [",", ";", "\t", "|"]
_HEADER_STYLES = ["snake_case", "Title Case", "UPPER"]


def export_to_csv(data: list[dict[str, Any]], path: str | Path) -> Path:
    """Export data to CSV with randomized delimiter, quoting, and column layout."""
    dest = Path(path).with_suffix(".csv")
    dest.parent.mkdir(parents=True, exist_ok=True)

    delimiter = random.choice(_DELIMITERS)
    header_style = random.choice(_HEADER_STYLES)
    include_headers = random.choices([True, False], weights=[90, 10])[0]
    flatten_metadata = random.choice([True, False])
    include_rules = random.choice([True, False])

    base_cols = ["input", "output"]
    if include_rules:
        base_cols.insert(0, "transformation_rules")

    if flatten_metadata:
        meta_keys: list[str] = []
        for entry in data:
            for k in (entry.get("metadata") or {}):
                if k not in meta_keys:
                    meta_keys.append(k)
        all_cols = base_cols + meta_keys
    else:
        all_cols = base_cols + (["metadata"] if any(e.get("metadata") for e in data) else [])

    random.shuffle(cols := list(all_cols))
    headers = [style_header(c, header_style) for c in cols]

    quoting = random.choice([csv.QUOTE_ALL, csv.QUOTE_MINIMAL, csv.QUOTE_NONNUMERIC])

    with dest.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter, quoting=quoting)
        if include_headers:
            writer.writerow(headers)
        for entry in data:
            row = []
            for col in cols:
                if col == "transformation_rules":
                    rules = entry.get("transformation_rules", [])
                    row.append("; ".join(rules) if isinstance(rules, list) else str(rules))
                elif col == "metadata":
                    row.append(json.dumps(entry.get("metadata", {})))
                elif col in ("input", "output"):
                    row.append(entry.get(col, ""))
                else:
                    meta = entry.get("metadata") or {}
                    val = meta.get(col, "")
                    row.append(json.dumps(val) if isinstance(val, (list, dict)) else str(val))
            writer.writerow(row)

    return dest
