# Coverage Report Template

Template for the coverage matrix produced by the coverage analysis phase. This report maps existing client I/O pairs against the ruleset's documented edge cases and variation dimensions, flagging gaps for downstream generation.

---

## Report Structure

The coverage report is a markdown file saved to `[output_dir]/coverage-report.md`. It contains four sections:

### 1. Summary

```markdown
## Coverage Report: [Domain Name]

**Ruleset:** [path to ruleset file]
**Client data source:** [path to JSON/CSV/folder]
**Samples analyzed:** [N]
**Edge cases defined:** [M]
**Coverage:** [X/M] ([percentage]%)
**Gaps found:** [G]

**Generated:** [timestamp]
```

### 2. Coverage Matrix

The core output. One row per documented edge case from the ruleset.

```markdown
## Coverage Matrix

| # | Edge Case | Source | Covered? | Existing Example | Suggested Addition |
|---|-----------|--------|----------|------------------|--------------------|
| 1 | Empty input | ruleset L42 | Yes | sample_003.json | -- |
| 2 | Multi-language input | ruleset L58 | No | -- | Generate: mixed EN/DE input with DE job description |
| 3 | Rate limit exceeded | api-spec.md L91 | No | -- | Generate: 429 response handling |
| 4 | Exact threshold match | ruleset L407 | Partial | sample_007.json (experience only) | Generate: threshold match for education requirement |
```

**Column definitions:**

- **Edge Case**: The documented edge case name from the ruleset's EDGE CASES section or variation dimension slots
- **Source**: Where the edge case is defined — ruleset line reference or requirements doc reference
- **Covered?**: `Yes` (at least one existing sample covers this case), `Partial` (sample touches this case but doesn't fully exercise it), or `No` (no existing sample)
- **Existing Example**: File name or sample ID of the matching client I/O pair(s). `--` if none
- **Suggested Addition**: Concrete, one-line description of what to generate. Must be specific enough for a generation subagent to act on. `--` if already covered

### 3. Variation Dimension Coverage

One table per variation dimension from the ruleset. Shows which slots are covered by existing data vs. missing.

```markdown
## Variation Dimension Coverage

### candidate_profile
| Slot | Target % | Existing Count | Covered? |
|------|----------|----------------|----------|
| strong_match | 25% | 4 | Yes |
| good_match | 20% | 2 | Yes |
| borderline | 15% | 0 | No |
| weak_match | 15% | 1 | Yes |
| career_changer | 10% | 0 | No |
| overqualified | 10% | 0 | No |
| junior_mismatch | 5% | 0 | No |

### job_domain
| Slot | Target % | Existing Count | Covered? |
|------|----------|----------------|----------|
| software_engineering | 30% | 5 | Yes |
| data_ai | 15% | 0 | No |
| ... | ... | ... | ... |
```

### 4. Additive Generation Brief

A summary of all gaps, formatted as a generation brief that LAB-112 (or create-data's generation phase) can consume directly.

```markdown
## Additive Generation Brief

**Total gaps:** [N]
**Suggested new samples:** [M]

### Priority Gaps (no coverage at all)

1. **Borderline candidate profile** — No existing samples. Generate: candidate who meets 60% of requirements with strong soft skills but missing one must-have.
2. **Career changer profile** — No existing samples. Generate: marketing professional applying for data science role with transferable analytical skills.
3. **Data/AI job domain** — No existing samples. Generate: ML engineer or data scientist job description with technical screening criteria.

### Partial Coverage (needs additional examples)

4. **Exact threshold edge case** — 1 sample covers experience threshold only. Generate: threshold match for education requirement (e.g., "Bachelor's required", candidate has Bachelor's exactly).

### Well-Covered (no action needed)

- Strong match (4 samples)
- Software engineering domain (5 samples)
- Empty input edge case (1 sample)
```

---

## Classification Logic

### How to classify a client sample against ruleset targets

For each client I/O pair, determine which coverage targets and variation slots it covers.

**Where to find targets in a v2 ruleset (schema_version: "2.0"):**
- **Coverage categories** → PER-CATEGORY COMPOSITION section (happy_path, edge_case, error_case, adversarial profiles)
- **Variation dimensions** → INPUT SCHEMA → Presentation and Variation tables per entity, plus the `composition` YAML block
- **Pairing types** → PAIRING STRATEGY section (if multi-entity)
- **Edge case scenarios** → described within PER-CATEGORY COMPOSITION's edge_case and adversarial profiles, and in FEW-SHOT EXAMPLES
- **Distribution targets** → PLANNING YAML → `coverage_distribution`

**Classification steps:**

1. **Read the sample's input and output** — understand what scenario it represents
2. **Determine coverage category** — does this sample match a happy_path, edge_case, error_case, or adversarial profile from PER-CATEGORY COMPOSITION?
3. **Map variation dimension slots** — for each dimension in the INPUT SCHEMA Variation tables, which slot does this sample represent?
4. **Map pairing type** (if multi-entity) — which pairing type from PAIRING STRATEGY does this sample match?
5. **Assign coverage**: A sample can cover multiple dimension slots but typically maps to one coverage category

### Coverage determination rules

- **Yes**: At least one sample fully exercises the edge case — both the input scenario AND the expected output behavior match
- **Partial**: A sample touches the scenario but doesn't fully exercise it (e.g., threshold match for experience but not education)
- **No**: No sample comes close to the described scenario

### Additive-only constraint

Every suggested addition MUST be verified against all existing samples:
- No suggestion should describe a scenario already covered by an existing sample
- Suggestions must be specific enough to avoid accidental overlap during generation
- When in doubt, mark as "Partial" rather than "No" — false negatives (missing a gap) are less harmful than false positives (flagging a covered case as missing)

---

## Input Format Support

The coverage analyzer accepts client I/O pairs in three formats:

### JSON Array
```json
[
  {
    "input": "...",
    "output": "...",
    "metadata": {}
  }
]
```
Also accepts the standard generated format with `transformation_rules` field.

### CSV File
```csv
input,output,metadata
"multi-line input text","multi-line output text","{optional JSON}"
```
Columns named `input` and `output` (case-insensitive). Additional columns treated as metadata.

### Folder of Files
```
samples/
  sample_1/
    input_data/
      document_a.pdf
      document_b.txt
    output_data/
      result.json
  sample_2/
    input_data/
      ...
    output_data/
      ...
```
Each subdirectory is one sample. `input_data/` contains input files, `output_data/` contains expected output. Also supports flat folders where each `.json` file is a self-contained sample.

---

## Output Location

Coverage reports are saved to the client-scoped path (matching SKILL.md's folder structure):
- **Client-scoped**: `dataset/[client]/[use-case]/augmented/coverage-report.md`
- **Fallback** (no client): `dataset/augmented/[domain_name]/coverage-report.md`

Create the directory if it doesn't exist.
