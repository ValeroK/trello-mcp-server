# MCP Configuration Setup Guide

This guide explains how to configure the Trello MCP Server with various MCP clients (Claude Desktop, Cursor, etc.) using Docker.

## Overview

The Trello MCP Server can be run in two modes:
1. **Claude App Mode (stdio)**: Direct integration with Claude Desktop using stdio transport
2. **SSE Server Mode**: HTTP/SSE server for other clients like Cursor

This setup uses Docker to run the server, making it easy to deploy and manage.

**Key Feature**: Environment variables (API credentials) are configured directly in the MCP configuration file (`mcp.json`), making the setup self-contained and portable.

---

## Prerequisites

1. **Docker**: Make sure Docker is installed and running
   ```bash
   docker --version
   ```

2. **Trello API Credentials**: Get your API key and token from [Trello Power-Ups Admin](https://trello.com/power-ups/admin)
   - Create a new integration
   - Copy your API key
   - Generate a token (click "Token" on the API key page)

3. **MCP Client**: Claude Desktop, Cursor, or another MCP-compatible client

---

## Setup for Claude Desktop

### Step 1: Configure Claude Desktop

Add the following configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "trello-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
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

**Important**: 
- Replace `your_trello_api_key_here` and `your_trello_token_here` with your actual Trello credentials
- All configuration is in the MCP config file - no separate `.env` file needed!
- The `env` section passes environment variables to the Docker container

### Step 2: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Start Claude Desktop again
3. The Trello MCP Server will automatically start when Claude initiates

### Step 3: Verify

In Claude Desktop, try asking:
- "Show me all my Trello boards"
- "What lists are in my board?"

---

## Setup for Cursor

### Step 1: Configure Cursor MCP

Edit your Cursor MCP config file:

**macOS/Linux**: `~/.cursor/mcp.json`  
**Windows**: `%USERPROFILE%\.cursor\mcp.json`

Add the following configuration:

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

**Important**: 
- Replace `your_trello_api_key_here` and `your_trello_token_here` with your actual credentials
- All configuration is in the MCP config file
- Docker runs in **interactive stdio mode** (not detached)
- The `-i` flag keeps the container running for communication
- The `--rm` flag automatically removes the container when it stops

### Step 2: Verify

In Cursor:
- Open the MCP panel (View → Model Context Protocol)
- You should see "trello-mcp-server" listed
- Try asking: "Show me my Trello boards"
- The Docker container runs in interactive mode and communicates via stdio

### Managing the Server

```bash
# View logs
docker logs -f trello-mcp-server

# Stop the server (if needed)
docker stop trello-mcp-server

# Or use the helper script
./stop-mcp-docker.sh

# Manual restart
./start-mcp-docker.sh
```

---

## Setup for Other MCP Clients

For other MCP-compatible clients, you have two options:

### Option 1: Configure in MCP Client

If your client supports command-based MCP servers:

```json
{
  "mcpServers": {
    "trello-mcp-server": {
      "command": "bash",
      "args": [
        "/path/to/start-mcp-docker.sh",
        "--from-config"
      ],
      "env": {
        "TRELLO_API_KEY": "your_api_key",
        "TRELLO_TOKEN": "your_token",
        "USE_CLAUDE_APP": "false",
        "MCP_SERVER_HOST": "127.0.0.1",
        "MCP_SERVER_PORT": "8952"
      }
    }
  }
}
```

### Option 2: Manual Start with .env File

1. Create a `.env` file:
   ```bash
   cp ".env example" .env
   # Edit .env with your credentials
   ```

2. Start the server:
   ```bash
   ./start-mcp-docker.sh
   ```

3. Connect your client to: `http://localhost:8952/sse`

---

## Configuration Options

Configuration is done through the MCP config file's `env` section. The startup script supports two methods (in priority order):

1. **Environment variables from MCP config** (recommended)
2. **`.env` file** (fallback for manual starts)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TRELLO_API_KEY` | Your Trello API key | - | ✅ Yes |
| `TRELLO_TOKEN` | Your Trello API token | - | ✅ Yes |
| `USE_CLAUDE_APP` | Use Claude App mode (stdio) | `false` | No |
| `MCP_SERVER_NAME` | Display name for the server | `Trello MCP Server` | No |
| `MCP_SERVER_HOST` | Server host address | `127.0.0.1` | No |
| `MCP_SERVER_PORT` | Server port | `8952` | No |

### Configuration Priority

The script loads configuration in this order (highest to lowest priority):
1. Environment variables passed from MCP config
2. Variables from `.env` file (if exists)
3. Default values

---

## Troubleshooting

### Docker Image Won't Pull

```bash
# Try pulling manually
docker pull ghcr.io/valerok/trello-mcp-server:latest

# Check Docker Hub status
docker info
```

### Container Won't Start

```bash
# Check logs
docker logs trello-mcp-server

# Verify environment variables are being passed
docker inspect trello-mcp-server | grep -A 20 Env

# Check if port is already in use
lsof -i :8952  # macOS/Linux
netstat -ano | findstr :8952  # Windows
```

### Authentication Errors

If you see 401 Unauthorized errors:

1. Verify your credentials in the MCP config file (`mcp.json`)
2. Make sure you're using the actual credentials, not placeholder text
3. Generate a new token at: https://trello.com/1/authorize?expiration=never&name=Trello+Assistant+MCP&scope=read,write&response_type=token&key=YOUR_API_KEY
4. Update the `env.TRELLO_TOKEN` value in your MCP config
5. Restart your MCP client (Claude Desktop/Cursor)

### Claude Desktop Not Connecting

1. Ensure the config file path is correct
2. Check that your credentials are properly escaped in JSON
3. Restart Claude Desktop completely (not just close window)
4. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

### Cursor Not Connecting

1. Ensure the Docker container is running: `docker ps`
2. Test the endpoint: `curl http://localhost:8952/health`
3. Check firewall settings
4. Try restarting Cursor

---

## Advanced Configuration

### Using Docker Compose

If you prefer Docker Compose:

```bash
# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Custom Port

To use a different port, update the `MCP_SERVER_PORT` in your MCP config:

```json
{
  "mcpServers": {
    "trello-mcp-server": {
      ...
      "env": {
        ...
        "MCP_SERVER_PORT": "9000"
      }
    }
  }
}
```

Then restart your MCP client.

### Network Configuration

The default setup uses `--network host` for simplicity. For custom networking:

1. Edit `start-mcp-docker.sh`
2. Replace `--network host` with custom bridge network
3. Update port mappings accordingly

---

## Getting Help

- **Documentation**: See [README.md](./README.md) for full documentation
- **Issues**: Report issues at the GitHub repository
- **Logs**: Always check `docker logs trello-mcp-server` first

---

## Quick Reference

```bash
# Start server
./start-mcp-docker.sh

# Stop server
./stop-mcp-docker.sh

# View logs
docker logs -f trello-mcp-server

# Pull latest image
docker pull ghcr.io/valerok/trello-mcp-server:latest

# Remove container
docker rm -f trello-mcp-server

# Health check
curl http://localhost:8952/health
```

