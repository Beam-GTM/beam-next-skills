# Documentation Template Guide

This guide explains the documentation template structure and how to customize it.

## Template Structure

The generated documentation follows this standardized format:

### 1. Header & Properties
```markdown
# 🤖 [Agent Name]

## Properties
- Agent Template
- Feasibility Status
- Priority Level
- Platform Status
- Vertical/Team
- Description
- Owner
- Internal Notes
```

### 2. Core Sections
- **Description**: What the agent does
- **Trigger**: How it's initiated
- **Workflow**: Step-by-step process
- **Data Inputs**: Required parameters
- **Expected Outputs**: Generated results
- **Key Integrations**: External services

### 3. Implementation Details
- Summary information
- Setup instructions
- Technical specifications
- Node breakdown
- Error handling

## Customization

### Adding Custom Sections
Edit `document_agent.py` and modify the `generate_markdown_documentation()` function:

```python
# Add after workflow section
lines.append("### Custom Section\n")
lines.append("Your custom content here\n")
lines.append("\n---\n")
```

### Modifying Property Fields
Update the Properties section template:

```python
lines.append(f"- **Custom Field**: {custom_value}")
```

### Integration Detection
Add new integrations to detect in `analyze_graph()`:

```python
for integration in ['Airtable', 'Gmail', 'YourNewIntegration']:
    if integration in tool_name:
        analysis['integrations'].add(integration)
```

## Placeholders

Auto-generated documentation includes placeholders for manual review:

- `[To be determined]` - Needs assignment
- `[Description needed]` - Requires detailed explanation
- `[Auto-generated - please review]` - Verify accuracy
- `[Add context here]` - Include additional information

Always review and replace these before finalizing documentation.

## Best Practices

1. **Review Workflow Steps**: Ensure they're in logical execution order
2. **Describe Inputs/Outputs**: Add meaningful descriptions for each field
3. **Document Integrations**: Explain how external services are used
4. **Add Scenarios**: Include real-world usage examples
5. **Test Instructions**: Verify setup steps are accurate

## Template Variables

Available data from graph analysis:

- `analysis['info']` - Agent metadata
- `analysis['nodes']` - Node configurations
- `analysis['integrations']` - Detected services
- `analysis['inputs']` - User input parameters
- `analysis['outputs']` - Generated outputs
- `analysis['connections']` - Node relationships

## Example Enhancements

### Add Scenario Template
```markdown
### Scenario: [Name]

**Description:** [What this scenario demonstrates]

**Input:**
- parameter1: value1
- parameter2: value2

**Expected Output:**
- result1: description
- result2: description

**Agent Behavior:**
- Step 1 behavior
- Step 2 behavior
```

### Add Troubleshooting Section
```markdown
## Troubleshooting

**Issue:** [Common problem]
**Solution:** [How to fix]

**Issue:** [Another problem]
**Solution:** [Resolution steps]
```

## Formatting Tips

- Use **bold** for field names and emphasis
- Use `code blocks` for technical values
- Use bullet lists for items without specific order
- Use numbered lists for sequential steps
- Use `---` dividers between major sections
- Use emoji sparingly (🤖 for agent, 🔗 for integrations, etc.)
