import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.server.fastmcp import Context
from server.tools.card import get_card, get_cards, create_card, update_card, delete_card, move_card
from server.models import TrelloCard
from server.dtos.update_card import UpdateCardPayload

@pytest.fixture
def mock_context():
    return MagicMock(spec=Context)

@pytest.fixture
def mock_service(mocker):
    return mocker.patch("server.tools.card.service", autospec=True)

@pytest.mark.asyncio
async def test_get_card_tool(mock_context, mock_service):
    card_id = "card123"
    expected_card = TrelloCard(
        id=card_id, 
        name="Test Card", 
        idList="l1", 
        idBoard="b1", 
        url="http://url", 
        pos=1.0
    )
    mock_service.get_card.return_value = expected_card

    result = await get_card(mock_context, card_id)

    assert result == expected_card
    mock_service.get_card.assert_called_once_with(card_id)

@pytest.mark.asyncio
async def test_get_cards_tool_list(mock_context, mock_service):
    list_id = "l1"
    expected_cards = [
        TrelloCard(
            id="c1", 
            name="C1", 
            idList=list_id, 
            idBoard="b1", 
            url="http://url", 
            pos=1.0
        )
    ]
    mock_service.get_cards.return_value = expected_cards

    result = await get_cards(mock_context, list_id)

    assert result == expected_cards
    mock_service.get_cards.assert_called_once_with(list_id)

@pytest.mark.asyncio
async def test_get_cards_tool_by_ids(mock_context, mock_service):
    card_ids = ["c1", "c2"]
    expected_card1 = TrelloCard(
        id="c1", 
        name="C1", 
        idList="l1", 
        idBoard="b1", 
        url="http://url", 
        pos=1.0
    )
    expected_card2 = TrelloCard(
        id="c2", 
        name="C2", 
        idList="l1", 
        idBoard="b1", 
        url="http://url", 
        pos=2.0
    )
    
    mock_service.get_card.side_effect = [expected_card1, expected_card2]

    result = await get_cards(mock_context, list_id="dummy", card_ids=card_ids)

    assert len(result) == 2
    assert result[0] == expected_card1
    assert result[1] == expected_card2
    assert mock_service.get_card.call_count == 2

@pytest.mark.asyncio
async def test_create_card_tool(mock_context, mock_service):
    list_id = "l1"
    name = "New Card"
    desc = "Desc"
    expected_card = TrelloCard(
        id="c1", 
        name=name, 
        desc=desc, 
        idList=list_id, 
        idBoard="b1", 
        url="http://url", 
        pos=1.0
    )
    mock_service.create_card.return_value = expected_card

    result = await create_card(mock_context, list_id, name, desc)

    assert result == expected_card
    mock_service.create_card.assert_called_once_with(list_id, name, desc)

@pytest.mark.asyncio
async def test_update_card_tool(mock_context, mock_service):
    card_id = "c1"
    payload = UpdateCardPayload(name="Updated Name")
    expected_card = TrelloCard(
        id=card_id, 
        name="Updated Name", 
        idList="l1", 
        idBoard="b1", 
        url="http://url", 
        pos=1.0
    )
    mock_service.update_card.return_value = expected_card

    result = await update_card(mock_context, card_id, payload)

    assert result == expected_card
    mock_service.update_card.assert_called_once_with(card_id, name="Updated Name")

@pytest.mark.asyncio
async def test_delete_card_tool(mock_context, mock_service):
    card_id = "c1"
    expected_response = {"status": "success"}
    mock_service.delete_card.return_value = expected_response

    result = await delete_card(mock_context, card_id)

    assert result == expected_response
    mock_service.delete_card.assert_called_once_with(card_id)

@pytest.mark.asyncio
async def test_move_card_tool(mock_context, mock_service):
    card_id = "c1"
    target_list_id = "l2"
    expected_card = TrelloCard(
        id=card_id, 
        name="C1", 
        idList=target_list_id, 
        idBoard="b1", 
        url="http://url", 
        pos=1.0
    )
    mock_service.update_card.return_value = expected_card

    result = await move_card(mock_context, card_id, target_list_id)

    assert result == expected_card
    mock_service.update_card.assert_called_once_with(card_id, idList=target_list_id)
