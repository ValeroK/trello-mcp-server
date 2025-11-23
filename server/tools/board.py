"""
This module contains tools for managing Trello boards.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloBoard
from server.services.board import BoardService
from server.trello import client
from server.mcp_instance import mcp
from server.utils.decorators import mcp_tool

logger = logging.getLogger(__name__)

service = BoardService(client)


@mcp.tool()
@mcp_tool
async def get_board(context: Context, board_id: str) -> TrelloBoard:
    """Retrieves a specific board by its ID.

    Args:
        board_id (str): The ID of the board to retrieve.

    Returns:
        TrelloBoard: The board object containing board details.
    """
    return await service.get_board(board_id)


@mcp.tool()
@mcp_tool
async def get_boards(context: Context) -> List[TrelloBoard]:
    """Retrieves all boards for the authenticated user.

    Returns:
        List[TrelloBoard]: A list of board objects.
    """
    return await service.get_boards()
