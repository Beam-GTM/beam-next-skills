#!/usr/bin/env python3
"""
Generate extended README overview table (skill name, owner, version, category)
from registry.yaml for the beam-next-skills repository.

Usage (from beam-next-skills repo root):
    python3 build_readme_overview.py
    python3 build_readme_overview.py --registry /path/to/registry.yaml
    python3 build_readme_overview.py --markdown   # print table only (for piping into README)

Output: Markdown section "## Skills overview" with a table of all skills.
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def load_registry(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Registry not found: {path}")
    with open(path, encoding="utf-8") as f:
        if yaml:
            return yaml.safe_load(f) or {}
        # Minimal fallback: would need manual parsing
        raise RuntimeError("PyYAML required: pip install pyyaml")


def table_row(name: str, owner: str, version: str, category: str) -> str:
    def esc(s: str) -> str:
        return (s or "").replace("|", "\\|").strip()

    return f"| {esc(name)} | {esc(owner)} | {esc(version)} | {esc(category)} |"


def generate_overview_markdown(registry: dict) -> str:
    skills = registry.get("skills", [])
    # Deduplicate by (name, category) so duplicate paths in registry yield one row
    seen = set()
    unique = []
    for s in skills:
        key = (s.get("name", ""), s.get("category", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(s)

    lines = [
        "## Skills overview",
        "",
        "Extended index with owner and version. See `registry.yaml` for the full machine-readable index.",
        "",
        "| Skill | Owner | Version | Category |",
        "|-------|-------|---------|----------|",
    ]
    for s in sorted(unique, key=lambda x: (x.get("category", ""), x.get("name", ""))):
        name = s.get("name", "")
        owner = s.get("author", "") or "—"
        version = str(s.get("version", "1.0"))
        category = s.get("category", "")
        lines.append(table_row(name, owner, version, category))
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate README overview table from registry.yaml"
    )
    parser.add_argument(
        "--registry", "-r",
        default="registry.yaml",
        help="Path to registry.yaml (default: ./registry.yaml)",
    )
    parser.add_argument(
        "--markdown", "-m",
        action="store_true",
        help="Print only the table block (for embedding in README)",
    )
    args = parser.parse_args()

    reg_path = Path(args.registry).resolve()
    try:
        registry = load_registry(reg_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("Run from beam-next-skills repo root after building registry, or pass --registry /path/to/registry.yaml", file=sys.stderr)
        sys.exit(1)

    out = generate_overview_markdown(registry)
    if args.markdown:
        print(out)
    else:
        count = len(registry.get("skills", []))
        print(f"# Generated from {reg_path} ({count} skills)", file=sys.stderr)
        print(out)


if __name__ == "__main__":
    main()
