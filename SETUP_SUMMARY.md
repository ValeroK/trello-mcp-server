# Trello MCP Server - Setup Summary

## ✅ Your Working Configuration

### Cursor Setup (Current)

**Location**: `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "trello-mcp-server": {
      "command": "/Users/kobi.valero/Projects/trello-mcp-server/mcp-cursor-wrapper.sh"
    }
  }
}
```

### How It Works

1. **Wrapper Script** (`mcp-cursor-wrapper.sh`):
   - Automatically checks if container is running
   - Starts container if needed using `start-mcp-docker.sh`
   - Connects to HTTP server via `mcp-remote`

2. **Startup Script** (`start-mcp-docker.sh`):
   - Loads credentials from `.env` file
   - Starts Docker container with HTTP server
   - Container runs with `--restart unless-stopped` for persistence

3. **Environment Variables** (`.env` file):
   ```env
   TRELLO_API_KEY=your_key
   TRELLO_TOKEN=your_token
   MCP_SERVER_NAME="Trello MCP Server"
   MCP_SERVER_PORT=8952
   MCP_SERVER_HOST=0.0.0.0
   USE_CLAUDE_APP=false
   ```

### Server Details

- **HTTP Endpoint**: `http://localhost:8952/sse`
- **Health Check**: `http://localhost:8952/health`
- **Container Name**: `trello-mcp-server`
- **Docker Image**: `ghcr.io/valerok/trello-mcp-server:latest`

## 📁 Project Files

### Active Files (In Use)
- ✅ `mcp-cursor-wrapper.sh` - Cursor startup wrapper
- ✅ `start-mcp-docker.sh` - Container startup script
- ✅ `stop-mcp-docker.sh` - Container stop script
- ✅ `.env` - Your credentials (keep secret!)
- ✅ `logs/` - Server logs directory

### Template Files (For Reference)
- 📄 `mcp-config-claude.json` - Claude Desktop example
- 📄 `mcp-config-cursor.json` - Cursor example
- 📄 `MCP_SETUP.md` - Detailed setup guide
- 📄 `QUICK_REFERENCE.md` - Quick reference
- 📄 `README.md` - Main documentation

### Configuration Files
- 📋 `docker-compose.yml` - Alternative Docker Compose setup
- 📋 `Dockerfile` - Docker image definition
- 📋 `pyproject.toml` - Python project config

## 🎯 Common Commands

```bash
# Start server manually
./start-mcp-docker.sh

# Stop server
./stop-mcp-docker.sh
# or
docker stop trello-mcp-server

# View logs
docker logs -f trello-mcp-server

# Check health
curl http://localhost:8952/health

# Restart container
docker restart trello-mcp-server
```

## 🔧 Troubleshooting

### Container not running?
```bash
docker ps -a | grep trello-mcp
./start-mcp-docker.sh
```

### Connection refused?
```bash
# Check if server is responding
curl http://localhost:8952/health

# Check container logs
docker logs trello-mcp-server
```

### Restart Cursor
- Quit completely (Cmd+Q)
- Reopen Cursor
- MCP will auto-start container

## 🔐 Security Notes

- ⚠️ **Never commit `.env` file** - Contains your API credentials
- ⚠️ The `.gitignore` file is configured to exclude `.env`
- ✅ Credentials are only in `.env`, not in `mcp.json` in this setup

## 📚 Additional Documentation

- **Full Setup Guide**: [MCP_SETUP.md](./MCP_SETUP.md)
- **Quick Reference**: [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)
- **Main README**: [README.md](./README.md)
- **Docker Info**: [DOCKER_METHODOLOGY.md](./DOCKER_METHODOLOGY.md)

---

**Last Updated**: October 23, 2025  
**Status**: ✅ Working Configuration




