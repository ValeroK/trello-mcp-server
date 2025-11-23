#!/bin/bash

# Trello MCP Server Docker Stop Script
# This script stops the running Docker container

set -e

CONTAINER_NAME="trello-mcp-server"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    print_warning "Container $CONTAINER_NAME does not exist"
    exit 0
fi

# Check if container is running
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    print_info "Stopping container $CONTAINER_NAME..."
    docker stop "$CONTAINER_NAME"
    print_info "✓ Container stopped successfully"
else
    print_warning "Container $CONTAINER_NAME is not running"
    print_info "Removing stopped container..."
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
    print_info "✓ Container removed"
fi




