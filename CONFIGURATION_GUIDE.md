# Trello MCP Server - Configuration Guide

## Simple Docker Configuration (Recommended) ⭐

The Trello MCP Server works exactly like other MCP servers - just run Docker directly with environment variables!

### Cursor Configuration

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

**That's it!** No wrapper scripts, no separate containers, no HTTP server needed.

### Claude Desktop Configuration

**File**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

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

## How It Works

1. **Docker runs in stdio mode** (`-i` flag) - communicates via stdin/stdout
2. **Auto-cleanup** (`--rm` flag) - container removes itself when stopped
3. **Environment variables** passed from `env` section in mcp.json
4. **USE_CLAUDE_APP=true** - tells the server to run in stdio mode (not HTTP)

This is the same pattern as other MCP servers like GitHub, WhatsApp, etc.

## Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TRELLO_API_KEY` | Your Trello API key | ✅ Yes |
| `TRELLO_TOKEN` | Your Trello API token | ✅ Yes |
| `USE_CLAUDE_APP` | Must be `"true"` for stdio mode | ✅ Yes |
| `MCP_SERVER_NAME` | Display name | No (default: "Trello MCP Server") |

## Getting Trello Credentials

1. Go to [Trello Power-Ups Admin](https://trello.com/power-ups/admin)
2. Click "New" to create a new integration
3. Fill in the required information
4. Copy your **API Key**
5. Click "Token" link to generate your **API Token**
6. Paste both into your MCP configuration

## Alternative: HTTP/SSE Mode

If you need an HTTP server (for browser access or other tools), use the startup scripts:

```bash
# Edit .env file with your credentials
cp ".env example" .env
# (edit .env)

# Start HTTP server
./start-mcp-docker.sh

# Server available at http://localhost:8952/sse
```

For HTTP mode, set `USE_CLAUDE_APP=false` in `.env`.

## Configuration Comparison

### Stdio Mode (Recommended for MCP Clients)
✅ Simple - just Docker command  
✅ No separate scripts needed  
✅ Auto-cleanup with `--rm`  
✅ Works like other MCP servers  
❌ Not accessible via HTTP/browser  

### HTTP/SSE Mode (For browser access)
✅ Accessible via browser  
✅ Can use with multiple clients  
✅ Persistent container  
❌ Requires startup script  
❌ More complex setup  

## Minimal Configuration

Just the essentials:

```json
{
  "mcpServers": {
    "trello-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--name", "trello-mcp-server",
        "-e", "TRELLO_API_KEY",
        "-e", "TRELLO_TOKEN",
        "-e", "USE_CLAUDE_APP",
        "ghcr.io/valerok/trello-mcp-server:latest"
      ],
      "env": {
        "TRELLO_API_KEY": "your_key",
        "TRELLO_TOKEN": "your_token",
        "USE_CLAUDE_APP": "true"
      }
    }
  }
}
```

## Security Best Practices

- ✅ Credentials are in `mcp.json` (usually in `~/.cursor/` or `~/.config/Claude/`)
- ✅ Not in project directory
- ✅ Not committed to git
- ✅ Each MCP client has its own config file

## Troubleshooting

### Container name conflict?

If you get "container name already in use":

```bash
docker stop trello-mcp-server
docker rm trello-mcp-server
# Then restart Cursor
```

### Wrong credentials?

Just update the `env` section in `mcp.json` and restart your MCP client.

### Want to switch between stdio and HTTP modes?

**Stdio mode** (for MCP clients):
- Set `USE_CLAUDE_APP: "true"`
- Use Docker directly in mcp.json

**HTTP mode** (for browser access):
- Set `USE_CLAUDE_APP: "false"` in `.env`
- Run `./start-mcp-docker.sh`

---

**See also**:
- [mcp-config-cursor.json](./mcp-config-cursor.json) - Template for Cursor
- [mcp-config-claude.json](./mcp-config-claude.json) - Template for Claude Desktop
- [README.md](./README.md) - Full documentation
