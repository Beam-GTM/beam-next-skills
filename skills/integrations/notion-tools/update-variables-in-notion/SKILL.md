---
name: update-variables-in-notion
version: '1.0'
description: Extract variables from Beam prompt chain files (.md) and sync to Notion
  database. Load when user mentions "extract variables", "prompt variables to notion",
  "update variables", "document variables", or provides a path to prompt files. Handles
  single files or directories. Creates/updates Notion database with variable metadata
  (name, description, data type, node).
author: Jack Li
category: general
tags:
- notion
- update
platform: Notion
updated: '2025-12-10'
visibility: team
---
# Update Variables in Notion

Extract `{VARIABLE_NAME}` patterns from Beam prompt chain files and sync to a Notion database for documentation and tracking.

## When to Use

Trigger this skill when:
- User provides a path to a prompt file or directory
- User mentions "extract variables", "update variables in notion"
- User wants to document prompt chain variables

## Workflow

### Step 1: Extract Variables

Run the extraction script on the provided path (single file or directory):

```bash
python3 scripts/extract_variables.py <path_to_file_or_directory>
```

**Output:** JSON with extracted variables including:
- `name`: Variable name (e.g., "RESUME_TEXT_PLACEHOLDER")
- `node`: Filename without extension (e.g., "1-extract-resume-data")
- `data_type`: Inferred type (string/number/boolean/array/object)
- `context`: Surrounding text (200 chars)
- `line_number`: Where variable appears in file

**Review the output** and note:
- Total variables found
- Inferred data types (verify accuracy)
- Any duplicates across nodes

### Step 2: Ask User for Notion Database

Ask user: "Should I create a new Notion database or update an existing one?"

**Option A - New Database:**
- Ask for database name (default: "Prompt Variables")
- Ask for parent page/location (or create as workspace-level page)
- Continue to Step 3A (Create New Database)

**Option B - Existing Database:**
- Ask for database URL or ID
- Fetch database using `mcp__notion__notion-fetch`
- Display current schema to user
- Continue to Step 2.5 (Schema Mapping)

### Step 2.5: Schema Mapping (For Existing Database Only)

**Fetch and analyze existing database:**

1. Use `mcp__notion__notion-fetch` to get database structure
2. Parse schema to identify:
   - Title property name (for variable name)
   - Available properties (Description, Data Type, Node, etc.)
   - Property types (rich_text, select, etc.)

3. **Display schema to user:**
   ```
   Found existing database schema:
   - Title property: "Name" (title)
   - "Description" (rich_text)
   - "Type" (select: string, number, boolean, array, object)
   - "Possible Values" (rich_text)
   - "Status" (select: to add, to confirm, done)
   - "Node Name" (rich_text)
   ```

4. **Ask for field mapping:**
   ```
   Let me map the extracted data to your database fields:

   Extracted fields → Database properties:
   - Variable name → "Name" (title) ✓
   - Data type → "Type" (select) ✓
   - Possible values → "Possible Values" (rich_text) ✓
   - Node name → "Node Name" (rich_text) ✓
   - Status → "Status" (select, default: "to add") ✓
   - Description → (leave empty for user to fill) ✓

   Does this mapping look correct?
   - "yes" - Continue with this mapping
   - "no" - I'll ask about each field individually
   ```

5. **If user says "no"**, ask for each mapping:
   ```
   Where should I put the variable name?
   Available fields: [list title properties]

   Where should I put the data type?
   Available fields: [list select/rich_text properties]

   Where should I put the node name?
   Available fields: [list text properties]
   ```

6. **Store mapping** for use in Step 4

### Step 3: Create/Update Notion Database

**For new database:**

Use `mcp__notion__notion-create-database` with properties:
```json
{
  "properties": {
    "Name": {"title": {}},
    "Description": {"rich_text": {}},
    "Data Type": {
      "select": {
        "options": [
          {"name": "string", "color": "blue"},
          {"name": "number", "color": "green"},
          {"name": "boolean", "color": "purple"},
          {"name": "array", "color": "orange"},
          {"name": "object", "color": "red"}
        ]
      }
    },
    "Possible Values": {"rich_text": {}},
    "Status": {
      "select": {
        "options": [
          {"name": "to add", "color": "gray"},
          {"name": "to confirm", "color": "yellow"},
          {"name": "done", "color": "green"}
        ]
      }
    },
    "Node": {"rich_text": {}}
  }
}
```

**For existing database:**

1. **Fetch database schema** using `mcp__notion__notion-fetch`
2. **Check for required fields**:
   - If "Possible Values" field missing: Add it using `mcp__notion__notion-update-database`
   - If "Status" field missing: Add it with options (to add, to confirm, done)
3. **Fetch all existing entries** using `mcp__notion__notion-search` with database URL
4. **Build list of existing variable names** (from title property)
5. **Compare with extracted variables:**
   ```
   Checking for duplicates...

   Found in database: RESUME_TEXT_PLACEHOLDER, JOB_DATA_OBJECT
   New variables: CANDIDATE_JSON_PLACEHOLDER, SMS_TEMPLATE_TEXT

   Duplicates: 2 variables already exist
   New: 2 variables to add
   ```

6. **Ask user how to handle duplicates:**
   ```
   How should I handle variables that already exist?

   Options:
   - "skip" - Skip all duplicates (default, safe)
   - "update" - Update existing entries (overwrites Data Type, Possible Values, and Node)
   - "ask" - Ask me for each duplicate individually
   ```

7. **Process based on user choice:**
   - **skip**: Only create entries for new variables
   - **update**: Use `mcp__notion__notion-update-page` for duplicates
   - **ask**: For each duplicate, ask: "Update [VARIABLE_NAME]? (yes/no)"

8. **Preserve existing content:**
   - NEVER overwrite Description or Status fields (user-filled content)
   - Only update Data Type, Possible Values, and Node if user chose "update"
   - Always skip if user chose "skip"

### Step 4: Populate Database

**Use field mapping** from Step 2.5 (or default if new database).

**For new variables** (not in database yet):

Use `mcp__notion__notion-create-pages` with mapped properties:

```json
{
  "parent": {"database_id": "<database_id>"},
  "pages": [{
    "properties": {
      "<mapped_title_property>": "<variable_name>",
      "<mapped_description_property>": "",
      "<mapped_datatype_property>": "<inferred_type>",
      "<mapped_possible_values_property>": "<extracted_possible_values>",
      "<mapped_status_property>": "to add",
      "<mapped_node_property>": "<node_name>"
    }
  }]
}
```

**For duplicate variables** (if user chose "update"):

Use `mcp__notion__notion-update-page` to update ONLY Data Type, Possible Values, and Node:

```json
{
  "page_id": "<existing_page_id>",
  "properties": {
    "<mapped_datatype_property>": "<inferred_type>",
    "<mapped_possible_values_property>": "<extracted_possible_values>",
    "<mapped_node_property>": "<node_name>"
    // DO NOT include Description or Status - preserve user content
  }
}
```

**Batch creation:** Group new variables into batches of 10-20 for efficient creation.

**Field handling:**
- **Description**: Auto-extracted from prompt Step-by-Step sections where possible; may be empty or generic for some fields (user should review and refine)
- **Possible Values**: Auto-populated from JSON schema (enums, formats, nullable types)
- **Status**: Set to "to add" for new entries (user updates as they document)
- **Object/Array types**: Description includes nested field structure (e.g., "Object with fields: name, email, phone...")
- Never update Description or Status for existing entries when mode is "update" (preserves user content)

**Description extraction notes:**
- Searches Step-by-Step instruction sections for field mentions
- Matches field names or components (e.g., "location" for "location_city")
- Some fields may have generic or missing descriptions if not explicitly documented in prompt
- **User should review and refine** all descriptions after initial sync

### Step 5: Confirm Completion

Report comprehensive results:

```
✅ Variables synced to Notion!

Summary:
- Total variables extracted: [N]
- New entries created: [X]
- Existing entries updated: [Y] (if update mode)
- Duplicates skipped: [Z] (if skip mode)
- Enum fields with possible values: [E]

Database: [Notion database URL]

Field mapping used:
- Variable names → [property name]
- Data types → [property name]
- Possible values → [property name] (auto-extracted from schema)
- Status → [property name] (default: "to add")
- Node names → [property name]
- Descriptions → (user-fillable)

Next steps:
- Review the database and add descriptions for new variables
- Verify data types and possible values are correct
- Update Status field as you document each variable
- Update any fields that need correction
```

**Remind user:** Descriptions are intentionally left empty for you to fill with context-specific information.

## Data Type Inference

The script infers data types using naming patterns and context. See [data-type-inference.md](references/data-type-inference.md) for detailed rules.

**Quick reference:**
- `{USER_COUNT}`, `{JOB_ID}` → number
- `{HAS_LICENSE}`, `{IS_QUALIFIED}` → boolean
- `{CANDIDATE_LIST}`, `{ITEMS_ARRAY}` → array
- `{CONFIG_JSON}`, `{USER_OBJECT}` → object
- Default → string

## Error Handling

**No variables found:**
- Verify file uses `{VARIABLE_NAME}` format (uppercase with underscores)
- Check file is .md format
- Confirm path is correct

**Notion database errors:**
- Verify user has write permissions
- Check database schema matches expected properties
- Ensure parent page exists if specified

**Duplicate handling:**
- Fetch existing entries before creating new ones
- Compare by variable name (case-sensitive match on title property)
- Three modes: skip (default), update, or ask
- When updating: ONLY update Data Type, Possible Values, and Node; NEVER update Description or Status
- Report all skipped/updated entries to user
- Preserves user-created content in Description and Status fields

## Example Usage

**Single file:**
```
User: "Extract variables from 02-projects/agent-1/prompts/extract-data.md and update in Notion"