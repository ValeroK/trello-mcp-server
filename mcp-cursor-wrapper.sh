#!/bin/bash

# MCP Cursor Wrapper Script
# This script ensures the Trello MCP Docker container is running before connecting
# Environment variables can be passed from MCP config:
#   TRELLO_API_KEY, TRELLO_TOKEN, MCP_SERVER_PORT, MCP_SERVER_HOST, etc.

set -e

CONTAINER_NAME="trello-mcp-server"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_PORT=${MCP_SERVER_PORT:-8952}

# Function to check if container is running with matching credentials
check_container_credentials() {
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        # Container is running, check if credentials match (if provided)
        if [ -n "$TRELLO_API_KEY" ]; then
            CONTAINER_KEY=$(docker inspect "$CONTAINER_NAME" --format '{{range .Config.Env}}{{println .}}{{end}}' | grep "TRELLO_API_KEY=" | cut -d= -f2)
            if [ "$CONTAINER_KEY" != "$TRELLO_API_KEY" ]; then
                echo "Container running with different credentials, restarting..." >&2
                docker stop "$CONTAINER_NAME" >&2
                docker rm "$CONTAINER_NAME" >&2
                return 1
            fi
        fi
        return 0
    fi
    return 1
}

# Check if container is running with correct credentials
if ! check_container_credentials; then
    echo "Starting Trello MCP Server container..." >&2
    
    # Check if container exists but is stopped
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        # If we have new credentials from MCP config, remove old container
        if [ -n "$TRELLO_API_KEY" ] && [ -n "$TRELLO_TOKEN" ]; then
            echo "Removing existing container to use new credentials..." >&2
            docker rm "$CONTAINER_NAME" >&2
        else
            echo "Container exists but stopped, starting it..." >&2
            docker start "${CONTAINER_NAME}" >&2
            sleep 3
        fi
    fi
    
    # If container doesn't exist, create it
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "Creating new container..." >&2
        
        # Export environment variables so the startup script can use them
        export TRELLO_API_KEY="${TRELLO_API_KEY}"
        export TRELLO_TOKEN="${TRELLO_TOKEN}"
        export MCP_SERVER_HOST="${MCP_SERVER_HOST:-0.0.0.0}"
        export MCP_SERVER_PORT="${MCP_SERVER_PORT:-8952}"
        export MCP_SERVER_NAME="${MCP_SERVER_NAME:-Trello MCP Server}"
        export USE_CLAUDE_APP="${USE_CLAUDE_APP:-false}"
        
        # Run startup script with --from-config flag
        "${SCRIPT_DIR}/start-mcp-docker.sh" --from-config >&2
    fi
    
    # Wait for server to be ready
    echo "Waiting for server to be ready..." >&2
    for i in {1..15}; do
        if curl -sf "http://localhost:${MCP_PORT}/health" >/dev/null 2>&1; then
            echo "Server is ready!" >&2
            break
        fi
        sleep 1
    done
fi

# Now connect via mcp-remote
exec npx -y mcp-remote "http://localhost:${MCP_PORT}/sse"

