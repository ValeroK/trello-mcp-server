import logging
from server.mcp_instance import mcp
import server.tools.board as board  # noqa: F401
import server.tools.card as card  # noqa: F401
import server.tools.list as list  # noqa: F401
import server.tools.checklist as checklist  # noqa: F401
import server.health_app  # noqa: F401

logger = logging.getLogger(__name__)

# Set httpx logger to ERROR to avoid leaking sensitive data
logging.getLogger("httpx").setLevel(logging.ERROR)

# Add a console handler for development
import sys

console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

if __name__ == "__main__":
    try:
        # Verify environment variables
        # Note: Settings validation ensures these exist at startup
        from server.config import settings

        if settings.USE_CLAUDE_APP:
            logger.info("Starting Trello MCP Server in Claude app mode...")
            mcp.run(transport="stdio")  # Explicitly use stdio transport for Claude
        else:
            logger.info(
                f"Starting Trello MCP Server in SSE mode at http://{settings.MCP_SERVER_HOST}:{settings.MCP_SERVER_PORT}/sse"
            )
            mcp.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
