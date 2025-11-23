# Trello MCP Server - Quick Reference

## Environment Variables (Configure in mcp.json)

```json
{
  "env": {
    "TRELLO_API_KEY": "your_api_key",       // Required: Get from trello.com/power-ups/admin
    "TRELLO_TOKEN": "your_token",           // Required: Generate from Trello
    "USE_CLAUDE_APP": "false",              // "true" for Claude Desktop, "false" for Cursor
    "MCP_SERVER_HOST": "127.0.0.1",         // Server host (localhost)
    "MCP_SERVER_PORT": "8952",              // Server port
    "MCP_SERVER_NAME": "Trello MCP Server"  // Display name
  }
}
```

## Configuration Files

| Client | Config File Location | Config Template |
|--------|---------------------|-----------------|
| **Cursor** | `~/.cursor/mcp.json` | `mcp-config-cursor.json` |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)<br>`%APPDATA%\Claude\claude_desktop_config.json` (Windows) | `mcp-config-claude.json` |
| **Other** | Client-specific | `mcp-config-example.json` |

## Quick Commands

```bash
# Make scripts executable (first time only)
chmod +x start-mcp-docker.sh stop-mcp-docker.sh

# Start server manually (uses .env as fallback)
./start-mcp-docker.sh

# Stop server
docker stop trello-mcp-server
# or
./stop-mcp-docker.sh

# View logs
docker logs -f trello-mcp-server

# Check health
curl http://localhost:8952/health

# Pull latest image
docker pull ghcr.io/valerok/trello-mcp-server:latest
```

## Configuration Priority

The startup script loads configuration in this order (highest to lowest):

1. **Environment variables from MCP config** (Recommended)
2. Variables from `.env` file (Fallback)
3. Default values

## Example: Cursor Configuration

**File**: `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "trello-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--name",
        "trello-mcp-server",
        "-e",
        "TRELLO_API_KEY",
        "-e",
        "TRELLO_TOKEN",
        "-e",
        "USE_CLAUDE_APP",
        "-e",
        "MCP_SERVER_NAME",
        "-e",
        "MCP_SERVER_HOST",
        "-e",
        "MCP_SERVER_PORT",
        "ghcr.io/valerok/trello-mcp-server:latest"
      ],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key_here",
        "TRELLO_TOKEN": "your_trello_token_here",
        "USE_CLAUDE_APP": "false",
        "MCP_SERVER_HOST": "127.0.0.1",
        "MCP_SERVER_PORT": "8952",
        "MCP_SERVER_NAME": "Trello MCP Server"
      }
    }
  }
}
```

**Steps**:
1. Add your Trello credentials
2. Save and restart Cursor
3. Docker runs in interactive stdio mode (not detached)

## Example: Claude Desktop Configuration

**File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "trello-mcp-server": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--name", "trello-mcp-server",
        "-e", "TRELLO_API_KEY",
        "-e", "TRELLO_TOKEN",
        "-e", "USE_CLAUDE_APP",
        "-e", "MCP_SERVER_NAME",
        "ghcr.io/valerok/trello-mcp-server:latest"
      ],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key_here",
        "TRELLO_TOKEN": "your_trello_token_here",
        "USE_CLAUDE_APP": "true",
        "MCP_SERVER_NAME": "Trello MCP Server"
      }
    }
  }
}
```

**Steps**:
1. Add your Trello credentials
2. Save and restart Claude Desktop

## Getting Trello Credentials

1. Go to https://trello.com/power-ups/admin
2. Create a new integration
3. Copy your **API Key**
4. Click "Token" to generate your **API Token**
5. Use these in your MCP configuration

## Troubleshooting

### Container not starting?
```bash
docker logs trello-mcp-server
```

### Check environment variables?
```bash
docker inspect trello-mcp-server | grep -A 20 Env
```

### Port already in use?
```bash
# macOS/Linux
lsof -i :8952

# Windows
netstat -ano | findstr :8952
```

### Authentication errors?
- Verify credentials are correct (not placeholder text)
- Generate a new token at Trello
- Update your MCP config
- Restart your MCP client

## Usage Examples

Once configured, you can ask your AI assistant:

- "Show me all my Trello boards"
- "What lists are in [board name]?"
- "Create a new card in [list name] with title [title]"
- "Move card [card name] to [list name]"
- "Update the description of card [card name]"
- "Add a checklist to card [card name]"
- "Show me all cards created since 2025-01-01"

## Server Endpoints (SSE Mode)

- **SSE Endpoint**: `http://localhost:8952/sse`
- **Health Check**: `http://localhost:8952/health`

---

📖 **For complete documentation, see [MCP_SETUP.md](./MCP_SETUP.md)**

