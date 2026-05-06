# Schema Inference from Existing Data

When existing data is discovered in the repo (augmented samples, seed data, gold standards), **infer the input and output schemas** before proceeding to ruleset creation or data generation. This replaces manual schema description and ensures the ruleset matches actual data.

---

## When to Run

Run schema inference whenever Phase 0/1 discovers **any** of:
- Structured sample directories (folders matching `sample_*/` containing `input_data/` and `output_data/` subdirectories)
- Generated JSON files (JSON files with arrays of input/output pairs, typically in augmented data directories)
- Seed data (JSON files in directories named `seed/`)
- Gold standards (directories named `gold-standards/` containing reference samples)

These are discovered during Phase 0/1 context search — use whatever paths the Explore subagent found for this client. Skip if no data exists for this domain — the user will describe the schema manually.

---

## Inference Procedure

### Step 1: Sample at least 2-3 data points

Read a representative set of samples to avoid inferring from a single outlier:
- If structured directories exist: read 2-3 `sample_*/input_data/` and `sample_*/output_data/` directories
- If a generated JSON exists: read 3-5 entries from the array
- If seed data exists: read 3-5 entries

### Step 2: Infer Input Schema

For each sample's input, determine:

| Property | What to detect | Examples |
|----------|---------------|----------|
| **Document count** | Single file or multiple files per sample | 1 PDF, or 2 PDFs (CV + JD) |
| **File types** | What formats the input documents are in | PDF, CSV, TXT, JSON, XLSX, PPTX, images |
| **Content structure** | Whether the content is structured (fields/tables) or unstructured (prose) | Structured invoice with line items vs. freeform email |
| **Key fields/sections** | What information the input contains | For a CV: name, experience, education, skills |
| **Presentation variety** | Whether samples show format/layout variation | All PDFs vs. mix of PDF/TXT/images |

### Step 3: Infer Output Schema

For each sample's output, determine:

| Property | What to detect | Examples |
|----------|---------------|----------|
| **Format** | Plain text, JSON, CSV, code, or other | JSON object, Python code string |
| **Nesting level** | Flat keys or nested structure | `{"score": 85}` (flat) vs. `{"scores": {"must_have": 85}}` (nested) |
| **Field inventory** | All fields with types and example values | `decision: string, star_rating: number, gaps: string[]` |
| **Value ranges** | Observed ranges for numeric/enum fields | `star_rating: 1-5`, `decision: "accept" | "reject"` |
| **Consistency** | Whether all samples follow the same schema | All samples have identical fields vs. optional fields |

### Step 4: Default Rules

- **Default to flat keys** unless the data is inherently nested (e.g., line items in an invoice, nested scoring breakdown). If nesting exists, preserve it.
- **Preserve actual file types** — don't normalize. If inputs are PDFs, the schema says PDF.
- **Note optional fields** — if a field appears in some samples but not others, mark it optional.

---

## Presentation Format

Present the inferred schemas **side-by-side** for user confirmation. Use this format:

```
## Inferred Data Structure

Based on [N] existing samples in `[path]`:

### Input Schema
- **Documents per sample**: [count] ([entity names])
- **File types**: [list with distribution if varied]
- **Structure**:
  - [Entity 1]: [format] — [key fields/sections]
  - [Entity 2]: [format] — [key fields/sections]

### Output Schema
- **Format**: [JSON / plain text / CSV / code]
- **Nesting**: [flat / nested — with reason if nested]
- **Fields**:
  | Field | Type | Example | Required |
  |-------|------|---------|----------|
  | field_name | string | "example value" | yes |
  | ... | ... | ... | ... |

Does this match your expectations? I'll use this structure for the ruleset.
```

---

## How Skills Use the Inferred Schema

### In create-ruleset
- Pre-populate the INPUT FRAMEWORK and OUTPUT FRAMEWORK sections
- Use detected file types for the Presentation layer of each entity
- Use detected fields for the Content layer
- Use detected nesting level for the output structure
- Skip asking the user about structure they've already confirmed

### In create-data
- Validate that the ruleset's schema matches the existing data
- Use the inferred structure to determine what file types to generate
- Ensure generated samples follow the same directory structure as existing ones
- Flag mismatches between the ruleset and the actual data structure

---

## Supported Format Combinations

The inference handles any combination, but common patterns include:

| Input Format | Output Format | Example Domain |
|-------------|--------------|----------------|
| PDF(s) | JSON | CV evaluation, invoice extraction |
| JSON | JSON | Data transformation, API testing |
| Plain text | JSON | Classification, entity extraction |
| CSV | JSON | Data analysis, anomaly detection |
| PDF + CSV | Plain text | Report generation |
| Images | JSON | Document OCR, visual QA |
| Mixed (PDF + TXT) | JSON | Multi-source extraction |
