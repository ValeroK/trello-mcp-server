"""
This module contains tools for managing Trello lists.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context

from server.models import TrelloList
from server.services.list import ListService
from server.trello import client
from server.mcp_instance import mcp
from server.utils.decorators import mcp_tool

logger = logging.getLogger(__name__)

service = ListService(client)


# List Tools
@mcp.tool()
@mcp_tool
async def get_list(ctx: Context, list_id: str) -> TrelloList:
    """Retrieves a specific list by its ID.

    Args:
        list_id (str): The ID of the list to retrieve.

    Returns:
        TrelloList: The list object containing list details.
    """
    return await service.get_list(list_id)


@mcp.tool()
@mcp_tool
async def get_lists(ctx: Context, board_id: str) -> List[TrelloList]:
    """Retrieves all lists on a given board.

    Args:
        board_id (str): The ID of the board whose lists to retrieve.

    Returns:
        List[TrelloList]: A list of list objects.
    """
    return await service.get_lists(board_id)


@mcp.tool()
@mcp_tool
async def create_list(
    ctx: Context, board_id: str, name: str, pos: str = "bottom"
) -> TrelloList:
    """Creates a new list on a given board.

    Args:
        board_id (str): The ID of the board to create the list in.
        name (str): The name of the new list.
        pos (str, optional): The position of the new list. Can be "top" or "bottom". Defaults to "bottom".

    Returns:
        TrelloList: The newly created list object.
    """
    return await service.create_list(board_id, name, pos)


@mcp.tool()
@mcp_tool
async def update_list(ctx: Context, list_id: str, name: str) -> TrelloList:
    """Updates the name of a list.

    Args:
        list_id (str): The ID of the list to update.
        name (str): The new name for the list.

    Returns:
        TrelloList: The updated list object.
    """
    return await service.update_list(list_id, name)


@mcp.tool()
@mcp_tool
async def delete_list(ctx: Context, list_id: str) -> TrelloList:
    """Archives a list.

    Args:
        list_id (str): The ID of the list to close.

    Returns:
        TrelloList: The archived list object.
    """
    return await service.delete_list(list_id)
