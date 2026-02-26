# Data Type Inference Guide

This reference explains how the `extract_variables.py` script infers data types from variable names and context.

## Inference Rules

The script uses heuristics based on naming patterns and surrounding context. It errs on the side of caution, defaulting to `string` when uncertain.

### Number Type

**Triggers:**
- Variable name contains: `_COUNT`, `_ID`, `_NUMBER`, `_YEAR`, `_AGE`, `_TOTAL`, `_AMOUNT`
- Context contains: "number", "integer", "count"

**Examples:**
- `{USER_COUNT}` → number
- `{JOB_ID}` → number
- `{TOTAL_YEARS}` → number

### Boolean Type

**Triggers:**
- Variable name starts with: `HAS_`, `IS_`, `SHOULD_`, `CAN_`, `ENABLE_`
- Context contains: "true", "false", "boolean"

**Examples:**
- `{HAS_LICENSE}` → boolean
- `{IS_QUALIFIED}` → boolean
- `{SHOULD_SEND_SMS}` → boolean

### Array Type

**Triggers:**
- Variable name contains: `_LIST`, `_ARRAY`, `_ITEMS`, `_COLLECTION`
- Context contains: "array", "list"

**Examples:**
- `{CANDIDATE_LIST}` → array
- `{JOB_ITEMS}` → array
- `{CERTIFICATIONS_ARRAY}` → array

### Object Type

**Triggers:**
- Variable name contains: `_OBJECT`, `_JSON`, `_PAYLOAD`, `_CONFIG`, `_METADATA`
- Context contains: "json", "object"

**Examples:**
- `{USER_OBJECT}` → object
- `{API_PAYLOAD}` → object
- `{CONFIG_JSON}` → object

### String Type (Default)

**Triggers:**
- None of the above patterns match
- Most generic/common type

**Examples:**
- `{RESUME_TEXT}` → string
- `{CANDIDATE_NAME}` → string
- `{MESSAGE_TEMPLATE}` → string

## Manual Override

The extracted data type is a suggestion. Review the output JSON and manually adjust types in the Notion database if the inference is incorrect.

## Context Analysis

The script captures 200 characters of context around each variable to help with manual review and description inference. Use this context to:

1. Verify the inferred data type is correct
2. Write meaningful descriptions for the Notion database
3. Understand how the variable is used in the prompt
