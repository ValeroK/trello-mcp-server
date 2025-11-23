"""
This module contains tools for managing Trello cards.
"""

import logging
from typing import List, Optional
from datetime import datetime

from mcp.server.fastmcp import Context

from server.models import TrelloCard
from server.services.card import CardService
from server.trello import client
from server.dtos.update_card import UpdateCardPayload
from server.mcp_instance import mcp
from server.utils.decorators import mcp_tool

logger = logging.getLogger(__name__)

service = CardService(client)


@mcp.tool()
@mcp_tool
async def get_card(context: Context, card_id: str) -> TrelloCard:
    """Retrieves a specific card by its ID.

    Args:
        card_id (str): The ID of the card to retrieve.

    Returns:
        TrelloCard: The card object containing card details.
    """
    return await service.get_card(card_id)


@mcp.tool()
@mcp_tool
async def get_cards(context: Context, list_id: str, from_date: Optional[str] = None, card_ids: Optional[List[str]] = None) -> List[TrelloCard]:
    """Retrieves all cards in a given list, or a specific set of cards by ID, optionally filtered by creation or last activity date.

    Args:
        list_id (str): The ID of the list whose cards to retrieve.
        from_date (str, optional): ISO 8601 date string. Only cards created or updated on/after this date are returned.
        card_ids (List[str], optional): List of card IDs to fetch. If provided, only these cards are returned.

    Returns:
        List[TrelloCard]: A list of card objects.
    """
    if card_ids:
        cards = []
        for card_id in card_ids:
            try:
                card = await service.get_card(card_id)
                cards.append(card)
            except Exception as e:
                await context.error(f"Failed to fetch card {card_id}: {str(e)}")
        result = cards
    else:
        result = await service.get_cards(list_id)
    
    if from_date:
        try:
            cutoff = datetime.fromisoformat(from_date)
        except Exception:
            await context.error(f"Invalid from_date format: {from_date}. Use ISO 8601 format.")
            return []
        filtered = []
        for card in result:
            created = card.creationDate
            updated = card.dateLastActivity
            if (created and created >= cutoff) or (updated and updated >= cutoff):
                filtered.append(card)
        return filtered
    return result


@mcp.tool()
@mcp_tool
async def create_card(
    context: Context, list_id: str, name: str, desc: str | None = None
) -> TrelloCard:
    """Creates a new card in a given list.

    Args:
        list_id (str): The ID of the list to create the card in.
        name (str): The name of the new card.
        desc (str, optional): The description of the new card. Defaults to None.

    Returns:
        TrelloCard: The newly created card object.
    """
    return await service.create_card(list_id, name, desc)


@mcp.tool()
@mcp_tool
async def update_card(
    context: Context, card_id: str, payload: UpdateCardPayload
) -> TrelloCard:
    """Updates a card's attributes.

    Args:
        card_id (str): The ID of the card to update.
        **kwargs: Keyword arguments representing the attributes to update on the card.

    Returns:
        TrelloCard: The updated card object.
    """
    return await service.update_card(
        card_id, **payload.model_dump(exclude_unset=True)
    )


@mcp.tool()
@mcp_tool
async def delete_card(context: Context, card_id: str) -> dict:
    """Deletes a card.

    Args:
        card_id (str): The ID of the card to delete.

    Returns:
        dict: The response from the delete operation.
    """
    return await service.delete_card(card_id)


@mcp.tool()
@mcp_tool
async def move_card(context: Context, card_id: str, target_list_id: str) -> TrelloCard:
    """
    Moves a card to a different list (column) by updating its idList.

    Args:
        card_id (str): The ID of the card to move.
        target_list_id (str): The ID of the target list (column).

    Returns:
        TrelloCard: The updated card object after moving.
    """
    return await service.update_card(card_id, idList=target_list_id)
