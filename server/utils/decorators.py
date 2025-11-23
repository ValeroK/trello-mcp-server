import logging
import traceback
from functools import wraps
from typing import Callable, Any

from mcp.server.fastmcp import Context

logger = logging.getLogger(__name__)


def mcp_tool(func: Callable) -> Callable:
    """
    Decorator for MCP tools to handle logging and error reporting.

    It logs the start and end of the function execution.
    If an exception occurs, it logs the error with traceback,
    sends the error to the MCP context, and re-raises the exception.
    """

    @wraps(func)
    async def wrapper(context: Context, *args, **kwargs) -> Any:
        tool_name = func.__name__
        try:
            logger.info(f"Starting {tool_name} with args: {args} kwargs: {kwargs}")
            result = await func(context, *args, **kwargs)
            logger.info(f"Successfully completed {tool_name}")
            return result
        except Exception as e:
            tb = traceback.format_exc()
            error_msg = f"Failed to execute {tool_name}: {str(e)}\nTraceback:\n{tb}"
            logger.error(error_msg)
            await context.error(error_msg)
            raise

    return wrapper
