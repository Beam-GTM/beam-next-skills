---
name: create-data
version: '1.0'
description: Generate synthetic training data from a ruleset file. Use when the user
  wants to create training examples, generate augmented data, or produce samples following
  defined rules.
author: Aqib Ansari
category: general
tags:
- create
updated: '2026-02-25'
visibility: team
argument-hint: <ruleset_path> [--samples N] [--threshold 0.8]
disable-model-invocation: false
allowed-tools: Read, Write, Glob, Grep, Bash
---
# Generate Synthetic Data from Ruleset

Generate unique, diverse data samples from a ruleset file using multi-LLM consensus evaluation.

## Arguments

Parse from `$ARGUMENTS`:
- **ruleset_path** (required): Path to the ruleset markdown file (e.g., `$1`)
- **--samples N** (optional): Number of samples to generate per batch (default: 10, max: 50)
- **--threshold X** (optional): Minimum consensus score (default: 0.8)
- **--format FMTS** (optional): Comma-separated output formats (default: `json`). Supported: `json`, `csv`, `pdf`, `docx`, `xls`. Example: `--format json,csv,pdf`

Examples:
- `/create-data dataset/rulesets/refund_analysis.md`
- `/create-data dataset/rulesets/code_gen.md --samples 25 --threshold 0.85`
- `/create-data dataset/rulesets/refund_analysis.md --format json,csv,pdf,docx,xls`

## Resources

- **Generation Prompt**: See [templates/generation.md](templates/generation.md)
- **Verification Prompt**: See [templates/verification.md](templates/verification.md)
- **Export Scripts**: See [scripts/](scripts/) directory (standalone, no package imports)
  - `scripts/export.py` - Main dispatcher & CLI entry point
  - `scripts/helpers.py` - Shared utilities
  - `scripts/csv_export.py` - CSV export with formatting variations
  - `scripts/xlsx_export.py` - XLSX export with styling variations
  - `scripts/pdf_export.py` - PDF export with layout variations
  - `scripts/docx_export.py` - DOCX export with document style variations

---

## Configuration Defaults

- **num_samples_to_generate**: 10 per batch
- **min_consensus_score**: 0.8 (80/100)
- **require_unanimous_pass**: true (all evaluators must agree)
- **require_minimum_evaluators**: 3

---

## Workflow

### Phase 1: Initialization

1. **Load ruleset** from provided path. If missing, suggest `/create-ruleset`
2. **Extract examples** from ruleset's FEW-SHOT EXAMPLES section
3. **Initialize tracking** for diversity matrix dimensions

### Phase 2: Data Generation (batches of 10)

For each batch:
1. Check diversity gaps vs target distribution
2. Use [generation prompt template](templates/generation.md) with:
   - Domain context and rules from ruleset
   - 2-3 rotated few-shot examples (formatted as below)
   - Request for underrepresented categories
3. Generate samples as JSON array
4. Deduplicate (reject if >80% similarity with existing)
5. Update diversity tracking

**Few-Shot Example Format:**
```
Example 0:

Input (text prompt):
{example.input}

Output (code string):
{example.output}

---
```

**Sample format (string-based, not dicts):**
```json
{
  "transformation_rules": ["rule1 from ruleset", "rule2"],
  "input": "multi-line text prompt as continuous string",
  "output": "multi-line code/response as continuous string",
  "metadata": {
    "request_type": "category from ruleset",
    "context_level": "minimal/standard/detailed/full",
    "complexity": "simple/standard/complex"
  }
}
```

### Phase 3: Multi-LLM Consensus Verification

For each sample, use [verification prompt template](templates/verification.md) with **3+ independent LLM evaluators**.

**Three Evaluation Dimensions:**
1. **quality_score** (0-100): Overall quality assessment
2. **will_execute_correctly** (boolean): Code validity check
3. **passes_ruleset** (boolean): Ruleset compliance

**Quality Score Scale:**
| Range | Meaning |
|-------|---------|
| 80-100 | High: Correct, efficient, follows best practices |
| 60-79 | Medium: Works but verbose or missing some practices |
| 40-59 | Low: Works but inefficient or has issues |
| <40 | Invalid: Incorrect, syntax errors, fails to execute |

**Consensus Pass Criteria:**
- All evaluators agree on `will_execute_correctly: true` (unanimous)
- Average `quality_score` >= threshold (default 80)
- Conservative approach: single failing evaluation rejects sample

### Phase 4: Output

Save to: `dataset/augmented/[ruleset_name]_generated.json`

```json
[
  {
    "transformation_rules": ["rule1", "rule2"],
    "input": "multi-line text prompt string",
    "output": "multi-line code string",
    "metadata": {
      "request_type": "...",
      "context_level": "...",
      "complexity": "...",
      "quality_score": 87,
      "consensus_scores": [85, 88, 88],
      "generated_at": "2024-01-15T10:30:00Z"
    }
  }
]
```

### Phase 4b: Export to Additional Formats

If `--format` includes formats other than `json`, export using the **self-contained** export script bundled with this skill.

**Steps:**
Run the export script from this skill's `scripts/` directory (only pass non-json formats):
```bash
python .claude/skills/create-data/scripts/export.py \
    dataset/augmented/[ruleset_name]_generated.json \
    --format csv,pdf,docx,xls
```

**Dependencies required:** `openpyxl`, `fpdf2`, `python-docx` (install via `pip install openpyxl fpdf2 python-docx` if missing).

**Format Variation Details:**

Each export produces uniquely formatted documents with randomized styling to mirror real-world production data diversity. Running the same export twice will produce different formatting.

| Format | Randomized Variations |
|--------|-----------------------|
| **CSV** | Delimiter (comma, semicolon, tab, pipe), header style (snake_case, Title Case, UPPER), column order, metadata flattened vs JSON blob, optional transformation_rules column, quoting style |
| **XLSX** | Color theme (5 palettes), single vs multi-sheet by request_type, filters, freeze panes, cell borders, alternating row colors, optional summary stats sheet, header font size |
| **PDF** | Layout (table, per-entry sections, compact overview), font (Helvetica, Courier, Times), optional cover page, optional header/footer with page numbers |
| **DOCX** | Document style (formal report, listing, memo), font family (Calibri, Arial, Times New Roman, Cambria), font size, table vs paragraph presentation, optional table of contents, page breaks, line spacing, accent color |

Exported files are saved alongside the JSON: `dataset/augmented/[ruleset_name]_generated.{csv,xlsx,pdf,docx}`

### Phase 5: Summary Report

```
=== Data Generation Summary ===
Ruleset: [name]
Generated: [total] | Verified: [passed] | Pass Rate: [X]%
Duplicates Removed: [count]

Consensus Configuration:
- Evaluators: 3
- Threshold: 0.8
- Unanimous Execution: Required

Diversity Distribution:
┌─────────────────┬──────────┬──────────┐
│ Dimension       │ Target   │ Actual   │
├─────────────────┼──────────┼──────────┤
│ Request Type    │          │          │
│ Context Level   │          │          │
│ Complexity      │          │          │
│ Edge Cases      │ ~10%     │          │
└─────────────────┴──────────┴──────────┘

Quality Metrics:
- Average Score: [X]
- Min/Max: [X]/[X]
- Unanimous Pass Rate: [X]%

Output saved to: dataset/augmented/[name]_generated.json
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Ruleset not found | Ask for path or suggest `/create-ruleset` |
| No examples | Ask user for 2-3 examples |
| High rejection (>50%) | Pause, ask user to review ruleset |
| Low diversity | Explicitly request underrepresented categories |
| Consensus failure | Log detailed scores, use for prompt improvement |

## Tips

1. **Rotate examples** - Don't use same few-shot examples every batch
2. **Track gaps** - Fill diversity gaps in each batch
3. **Learn from failures** - Use rejection reasons to improve prompts
4. **String-based data** - Always use multi-line strings for input/output, never dicts
5. **Edge cases** - Include ~10% edge cases for production realism
