import pytest
from unittest.mock import AsyncMock
from server.services.card import CardService
from server.models import TrelloCard

@pytest.fixture
def mock_client():
    return AsyncMock()

@pytest.fixture
def card_service(mock_client):
    return CardService(mock_client)

@pytest.mark.asyncio
async def test_get_card(card_service, mock_client):
    card_id = "card123"
    mock_data = {
        "id": card_id, 
        "name": "Test Card", 
        "idList": "list1", 
        "idBoard": "board1", 
        "url": "http://trello.com/c/123", 
        "pos": 100.0
    }
    mock_client.GET.return_value = mock_data

    card = await card_service.get_card(card_id)

    assert isinstance(card, TrelloCard)
    assert card.id == card_id
    assert card.name == "Test Card"
    mock_client.GET.assert_called_once_with(f"/cards/{card_id}")

@pytest.mark.asyncio
async def test_get_cards(card_service, mock_client):
    list_id = "list123"
    mock_data = [
        {
            "id": "card1", 
            "name": "Card 1", 
            "idList": list_id, 
            "idBoard": "board1", 
            "url": "http://trello.com/c/1", 
            "pos": 100.0
        },
        {
            "id": "card2", 
            "name": "Card 2", 
            "idList": list_id, 
            "idBoard": "board1", 
            "url": "http://trello.com/c/2", 
            "pos": 200.0
        }
    ]
    mock_client.GET.return_value = mock_data

    cards = await card_service.get_cards(list_id)

    assert len(cards) == 2
    assert isinstance(cards[0], TrelloCard)
    assert cards[0].id == "card1"
    mock_client.GET.assert_called_once_with(f"/lists/{list_id}/cards")

@pytest.mark.asyncio
async def test_create_card(card_service, mock_client):
    list_id = "list123"
    name = "New Card"
    desc = "Description"
    mock_data = {
        "id": "newcard", 
        "name": name, 
        "desc": desc, 
        "idList": list_id, 
        "idBoard": "board1", 
        "url": "http://trello.com/c/new", 
        "pos": 300.0
    }
    mock_client.POST.return_value = mock_data

    new_card = await card_service.create_card(list_id, name, desc)

    assert isinstance(new_card, TrelloCard)
    assert new_card.name == name
    assert new_card.desc == desc
    mock_client.POST.assert_called_once_with("/cards", data={"name": name, "idList": list_id, "desc": desc})

@pytest.mark.asyncio
async def test_update_card(card_service, mock_client):
    card_id = "card123"
    mock_data = {
        "id": card_id, 
        "name": "Updated Card", 
        "idList": "list1", 
        "idBoard": "board1", 
        "url": "http://trello.com/c/123", 
        "pos": 100.0
    }
    mock_client.PUT.return_value = mock_data

    updated_card = await card_service.update_card(card_id, name="Updated Card")

    assert updated_card.name == "Updated Card"
    mock_client.PUT.assert_called_once_with(f"/cards/{card_id}", data={"name": "Updated Card"})

@pytest.mark.asyncio
async def test_delete_card(card_service, mock_client):
    card_id = "card123"
    mock_data = {"limits": {}}
    mock_client.DELETE.return_value = mock_data

    response = await card_service.delete_card(card_id)

    assert response == mock_data
    mock_client.DELETE.assert_called_once_with(f"/cards/{card_id}")
