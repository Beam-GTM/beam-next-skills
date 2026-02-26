# Notion MCP Setup Guide

This guide helps users set up the Notion MCP server for Claude Code.

## Prerequisites

- Claude Code installed
- Notion workspace with admin access

## Step 1: Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Fill in details:
   - **Name**: `Claude Code Integration` (or any name)
   - **Associated workspace**: Select your workspace
   - **Type**: Internal integration
4. Click **"Submit"**
5. **Copy the Internal Integration Token** (starts with `secret_...`)
   - Keep this safe! You'll need it in Step 2

## Step 2: Configure Claude Code

1. Open Claude Code configuration file:
   - **macOS**: `~/.config/claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. Add Notion MCP server configuration:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-notion"
      ],
      "env": {
        "NOTION_API_KEY": "secret_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

3. Replace `secret_YOUR_TOKEN_HERE` with your integration token from Step 1

4. **Save the file**

## Step 3: Grant Integration Access to Pages

The integration needs explicit access to pages you want to work with.

1. Open the Notion page you want to access (e.g., Customer Onboarding template)
2. Click **"••• "** (three dots) in top right
3. Select **"Add connections"**
4. Find and select your integration (e.g., "Claude Code Integration")
5. Click **"Confirm"**

**Important**: Grant access to:
- The main onboarding template page
- Any parent pages/databases

## Step 4: Restart Claude Code

1. **Quit Claude Code completely**
2. **Restart Claude Code**
3. MCP server will initialize on startup

## Step 5: Verify Setup

Test if MCP is working:

```
Ask Claude: "Can you list my Notion pages?"
```

If Claude can see your pages, setup is complete! ✅

## Troubleshooting

### Error: "Notion MCP not found"
- Make sure you restarted Claude Code
- Check the config file for typos

### Error: "Authentication failed"
- Verify the integration token is correct
- Make sure there are no extra spaces in the token

### Error: "Page not found"
- Grant integration access to the page (Step 3)
- Wait a few seconds and try again

### Still having issues?
- Check Claude Code logs: Help → Show Logs
- Verify `npx` is installed: `npx --version` in terminal
