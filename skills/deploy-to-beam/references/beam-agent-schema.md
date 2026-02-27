# beam-agent.yaml Schema Reference

The `beam-agent.yaml` file defines a Beam Platform agent specification that can be deployed via `POST /agent-graphs/complete`. Place it in any skill directory alongside `SKILL.md`.

## Full Schema

```yaml
# Agent metadata
agent:
  name: "Agent Name"                      # Required. Display name in Beam Platform
  description: "What the agent does"      # Required. Used for discovery and AI routing
  personality: "How it communicates"       # Optional. Personality/tone instructions
  restrictions: "What it must NOT do"     # Optional. Safety guardrails
  prompts:                                # Optional. Example inputs for testing
    - "Example query 1"
    - "Example query 2"

# Workflow nodes (the agent graph)
nodes:
  - id: "unique-node-id"                 # Required. UUID or descriptive string
    objective: "What this node does"      # Required. Clear instruction for the LLM
    is_entry: true                        # Is this the first node? (exactly one required)
    is_exit: false                        # Is this the last node?
    x: 100                               # Optional. Canvas X coordinate
    y: 150                               # Optional. Canvas Y coordinate
    on_error: "STOP"                      # STOP | CONTINUE | RETRY
    auto_retry: false                     # Retry on failure?
    retry_count: 1                        # How many retries
    retry_wait_ms: 1000                   # Wait between retries
    evaluation_enabled: false             # Enable quality evaluation?
    evaluation_criteria:                  # If evaluation_enabled: true
      - "Output contains required data"
      - "Response is under 500 words"
    pull_attachments: true                # Pass task attachments to this node?

    # Tool configuration
    tool:
      name: "Human-readable tool name"   # Required
      function_name: "tool_func_id"      # Required. From Beam's tool catalog
      description: "What the tool does"  # Required
      model: "gpt-4o"                    # LLM model: gpt-4o, gpt-4o-mini, etc.
      prompt: "System prompt for node"   # Optional. Additional instructions
      requires_consent: false            # Require human approval?
      is_memory_tool: false              # Use agent memory?
      memory_lookup_instruction: ""      # If is_memory_tool: instructions for lookup

      input_params:
        - name: "param_name"            # Required. Parameter identifier
          description: "What this is"   # Required. Clear description
          type: "string"                # string | number | boolean | object | array
          fill_type: "ai_fill"          # How the value is determined:
                                        #   ai_fill  → LLM decides the value
                                        #   static   → hardcoded value
                                        #   linked   → from another node's output
          static_value: ""              # If fill_type=static: the value
          linked_node_id: ""            # If fill_type=linked: source node ID
          linked_param: ""              # If fill_type=linked: source param name
          required: true                # Is this required?
          example: "example value"      # Example for documentation
          position: 0                   # Order in the UI

      output_params:
        - name: "output_name"           # Required. Output identifier
          description: "What this is"   # Required
          type: "string"                # string | number | boolean | object | array
          is_array: false               # Is this an array?
          example: "example output"     # Example for documentation
          position: 0                   # Order in the UI

    # Edges (connections to other nodes)
    edges:
      - target: "next-node-id"          # Required. Target node ID
        condition: ""                   # Optional. Conditional routing expression
        name: "Edge Name"              # Optional. Human-readable edge name
        pull_attachments: true         # Pass attachments through this edge?
```

## Common Tool Function Names

These are some frequently used tools from the Beam Platform catalog.
Use `function_name` values exactly as shown.

| Category | Tool | function_name |
|----------|------|---------------|
| **Email** | Send Gmail | `send_gmail` |
| **Email** | Read Gmail | `read_gmail` |
| **CRM** | HubSpot Search | `hubspot_search_contacts` |
| **CRM** | HubSpot Create | `hubspot_create_contact` |
| **Calendar** | Google Calendar Create | `google_calendar_create_event` |
| **Storage** | Google Drive Upload | `google_drive_upload_file` |
| **Messaging** | Slack Send | `slack_send_message` |
| **Custom** | Custom GPT Action | `GPTAction_Custom_*` |

> **Note**: Tool function names may vary. Use the Beam dashboard or ask Beam to confirm exact names.
> The AI-guided deployment path (Workflow 1) handles tool matching automatically.

## Example: Simple Email Agent

```yaml
agent:
  name: "Email Summarizer"
  description: "Reads new emails and sends a daily summary digest"
  personality: "Professional and concise"
  restrictions: "Never forward or reply to emails without approval"
  prompts:
    - "Summarize today's important emails"

nodes:
  - id: "read-emails"
    objective: "Read the latest unread emails from Gmail inbox and extract subject, sender, and key content"
    is_entry: true
    is_exit: false
    tool:
      name: "Gmail Reader"
      function_name: "read_gmail"
      description: "Reads emails from Gmail inbox"
      model: "gpt-4o"
      input_params:
        - name: "query"
          description: "Gmail search query"
          type: "string"
          fill_type: "static"
          static_value: "is:unread newer_than:1d"
      output_params:
        - name: "emails"
          description: "List of emails with subject, sender, body"
          type: "object"
          is_array: true
    edges:
      - target: "summarize"

  - id: "summarize"
    objective: "Create a concise summary digest of all emails, grouped by priority"
    is_entry: false
    is_exit: false
    tool:
      name: "Summary Generator"
      function_name: "GPTAction_Custom_Summarizer"
      description: "Generates structured email summary"
      model: "gpt-4o"
      prompt: "Create a concise daily email digest. Group by: urgent, follow-up needed, FYI."
      input_params:
        - name: "emails"
          description: "Email data from previous step"
          type: "object"
          fill_type: "linked"
          linked_node_id: "read-emails"
          linked_param: "emails"
      output_params:
        - name: "summary"
          description: "Formatted email digest"
          type: "string"
    edges:
      - target: "send-digest"

  - id: "send-digest"
    objective: "Send the email digest to the user"
    is_entry: false
    is_exit: true
    tool:
      name: "Gmail Sender"
      function_name: "send_gmail"
      description: "Sends email via Gmail"
      model: "gpt-4o-mini"
      input_params:
        - name: "to"
          description: "Recipient email"
          type: "string"
          fill_type: "static"
          static_value: "user@example.com"
        - name: "subject"
          description: "Email subject"
          type: "string"
          fill_type: "static"
          static_value: "Daily Email Digest"
        - name: "body"
          description: "Email body (the digest)"
          type: "string"
          fill_type: "linked"
          linked_node_id: "summarize"
          linked_param: "summary"
      output_params:
        - name: "status"
          description: "Send status"
          type: "string"
```

## Mapping from SKILL.md to beam-agent.yaml

| SKILL.md Section | beam-agent.yaml Field |
|------------------|-----------------------|
| `name:` (frontmatter) | `agent.name` |
| `description:` (frontmatter) | `agent.description` |
| Workflow steps | `nodes[].objective` |
| Scripts/tools mentioned | `nodes[].tool.function_name` |
| Input/output descriptions | `nodes[].tool.input_params` / `output_params` |
| Error handling | `nodes[].on_error` |
