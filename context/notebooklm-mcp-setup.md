# NotebookLM MCP Server Configuration Guide

## Installation Status
As of 2026-01-29, the `notebooklm-mcp-server` Python package is being installed in your project's virtual environment.

## Configuration Instructions

### Step 1: Access MCP Configuration in Antigravity

1. Open Antigravity IDE
2. Locate the "**...**" dropdown menu at the top of the editor's agent panel
3. Click on "**Manage MCP Servers**"
4. Select "**View raw config**"
5. This will open the `mcp_config.json` file

### Step 2: Add NotebookLM Server

Add the following configuration to your `mcp_config.json`:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "python",
      "args": [
        "-m",
        "notebooklm_mcp_server"
      ],
      "env": {
        "PYTHONPATH": "c:\\Users\\isma_\\Desktop\\NEW PROJECT\\.venv\\Lib\\site-packages"
      }
    }
  }
}
```

### Step 3: Authentication Process

After adding the configuration:

1. Restart Antigravity or reload the MCP servers
2. The NotebookLM MCP server will attempt to connect
3. **A browser window will open automatically** asking you to log in to your Google account
4. **IMPORTANT**: You must complete the authentication in the browser
5. The server will extract session cookies to maintain the connection
6. Once authenticated, the server will have access to your NotebookLM notebooks

### Step 4: Verify Connection

After authentication:
- Check the MCP server status in Antigravity
- Try listing your NotebookLM notebooks to confirm the connection is active

## Security Notes

> [!WARNING]
> The NotebookLM MCP server uses reverse-engineered internal Google APIs. It's recommended to use a dedicated Google account for this integration.

> [!IMPORTANT]
> Changes to Google's internal APIs may cause the server to stop working. Monitor the `notebooklm-mcp-server` repository for updates.

## Available Capabilities

Once connected, the MCP server provides:
- **Notebook Management**: Create, list, select, update, and delete notebooks
- **Research Queries**: Ask questions based on your uploaded documents
- **Content Generation**: Create audio overviews, summaries, and content from your notes
- **Source Synchronization**: Automatically sync Google Drive sources

## Troubleshooting

If authentication fails:
1. Check that your Python environment is activated
2. Ensure the `notebooklm-mcp-server` package is properly installed
3. Try re-authenticating by restarting the MCP server
4. Check the Antigravity logs for detailed error messages
