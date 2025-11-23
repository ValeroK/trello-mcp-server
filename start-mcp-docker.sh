#!/bin/bash

# Trello MCP Server Docker Startup Script
# This script manages the Docker container for the Trello MCP Server
# It can receive environment variables from:
# 1. MCP configuration (passed as environment variables)
# 2. .env file (fallback)
# 3. Command line arguments

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_NAME="trello-mcp-server"
IMAGE_NAME="ghcr.io/valerok/trello-mcp-server:latest"
ENV_FILE="$SCRIPT_DIR/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Check if running from MCP config
FROM_CONFIG=false
if [[ "$1" == "--from-config" ]]; then
    FROM_CONFIG=true
    print_info "Starting from MCP configuration"
fi

# Function to load from .env file if it exists
load_env_file() {
    if [ -f "$ENV_FILE" ]; then
        print_info "Loading environment from .env file..."
        set -a
        source "$ENV_FILE"
        set +a
        return 0
    else
        return 1
    fi
}

# Priority order for environment variables:
# 1. Already set environment variables (from MCP config)
# 2. .env file (fallback)

# If not running from MCP config or if key variables are missing, try .env file
if [ "$FROM_CONFIG" = false ] || [ -z "$TRELLO_API_KEY" ] || [ -z "$TRELLO_TOKEN" ]; then
    if [ -z "$TRELLO_API_KEY" ] || [ -z "$TRELLO_TOKEN" ]; then
        print_warning "Required environment variables not found in MCP config"
        
        if load_env_file; then
            print_info "Using credentials from .env file"
        else
            print_error "Neither MCP config nor .env file provides required credentials"
            print_info ""
            print_info "Please either:"
            print_info "  1. Configure environment variables in your MCP config (mcp.json), OR"
            print_info "  2. Create a .env file with your credentials:"
            print_info ""
            print_info "     cp '$SCRIPT_DIR/.env example' '$ENV_FILE'"
            print_info "     # Then edit $ENV_FILE and add your credentials"
            print_info ""
            print_info "Get your Trello credentials from: https://trello.com/power-ups/admin"
            exit 1
        fi
    fi
else
    print_info "Using environment variables from MCP configuration"
fi

# Validate required environment variables
if [ -z "$TRELLO_API_KEY" ] || [ "$TRELLO_API_KEY" = "TRELLO_API_KEY" ] || [ "$TRELLO_API_KEY" = "your_trello_api_key_here" ]; then
    print_error "TRELLO_API_KEY is not properly set"
    print_info "Please update your MCP config or .env file with a valid Trello API key"
    print_info "Get your API key from: https://trello.com/power-ups/admin"
    exit 1
fi

if [ -z "$TRELLO_TOKEN" ] || [ "$TRELLO_TOKEN" = "TRELLO_TOKEN" ] || [ "$TRELLO_TOKEN" = "your_trello_token_here" ]; then
    print_error "TRELLO_TOKEN is not properly set"
    print_info "Please update your MCP config or .env file with a valid Trello token"
    print_info "Get your token from: https://trello.com/power-ups/admin"
    exit 1
fi

# Set defaults for optional variables
export MCP_SERVER_PORT=${MCP_SERVER_PORT:-8952}
export MCP_SERVER_HOST=${MCP_SERVER_HOST:-127.0.0.1}
export USE_CLAUDE_APP=${USE_CLAUDE_APP:-false}
export MCP_SERVER_NAME=${MCP_SERVER_NAME:-"Trello MCP Server"}

print_debug "Configuration:"
print_debug "  MCP_SERVER_PORT=$MCP_SERVER_PORT"
print_debug "  MCP_SERVER_HOST=$MCP_SERVER_HOST"
print_debug "  USE_CLAUDE_APP=$USE_CLAUDE_APP"
print_debug "  MCP_SERVER_NAME=$MCP_SERVER_NAME"

# Check if container is already running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    print_info "Container $CONTAINER_NAME already exists"
    
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        print_info "Container is running. Stopping it first..."
        docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
    fi
    
    print_info "Removing existing container..."
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi

# Pull the latest image
print_info "Pulling latest Docker image: $IMAGE_NAME"
if ! docker pull "$IMAGE_NAME" 2>/dev/null; then
    print_warning "Failed to pull Docker image, checking for local image..."
    if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
        print_error "No local image found. Please check your internet connection."
        exit 1
    fi
    print_info "Using existing local image"
fi

# Create logs directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/logs"

# Start the container
print_info "Starting Trello MCP Server container..."
print_info "Mode: $([ "$USE_CLAUDE_APP" = "true" ] && echo "Claude App (stdio)" || echo "SSE Server")"
print_info "Port: $MCP_SERVER_PORT"
print_info "Host: $MCP_SERVER_HOST"

docker run \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -d \
    -e "TRELLO_API_KEY=$TRELLO_API_KEY" \
    -e "TRELLO_TOKEN=$TRELLO_TOKEN" \
    -e "USE_CLAUDE_APP=$USE_CLAUDE_APP" \
    -e "MCP_SERVER_NAME=$MCP_SERVER_NAME" \
    -e "MCP_SERVER_HOST=$MCP_SERVER_HOST" \
    -e "MCP_SERVER_PORT=$MCP_SERVER_PORT" \
    --network host \
    -v "$SCRIPT_DIR/logs:/app/logs" \
    "$IMAGE_NAME"

# Wait a moment for container to start
sleep 3

# Check if container is running
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    print_info "✓ Container started successfully"
    
    if [ "$USE_CLAUDE_APP" != "true" ]; then
        print_info "Server is available at: http://${MCP_SERVER_HOST}:${MCP_SERVER_PORT}/sse"
        print_info "Health check: http://${MCP_SERVER_HOST}:${MCP_SERVER_PORT}/health"
        
        # Test the health endpoint
        sleep 2
        if command -v curl >/dev/null 2>&1; then
            if curl -s "http://${MCP_SERVER_HOST}:${MCP_SERVER_PORT}/health" >/dev/null 2>&1; then
                print_info "✓ Health check passed"
            else
                print_warning "Health check endpoint not responding yet (may need more time to start)"
            fi
        fi
    fi
    
    print_info ""
    print_info "Useful commands:"
    print_info "  View logs:    docker logs -f $CONTAINER_NAME"
    print_info "  Stop server:  docker stop $CONTAINER_NAME"
    print_info "  Restart:      $0"
else
    print_error "Failed to start container. Checking logs..."
    docker logs "$CONTAINER_NAME" 2>&1 || true
    exit 1
fi

if [ "$FROM_CONFIG" = false ]; then
    print_info ""
    print_info "To view real-time logs, run: docker logs -f $CONTAINER_NAME"
fi
