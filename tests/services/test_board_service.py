import pytest
from unittest.mock import AsyncMock, MagicMock
from server.services.board import BoardService
from server.models import TrelloBoard

@pytest.fixture
def mock_client():
    return AsyncMock()

@pytest.fixture
def board_service(mock_client):
    return BoardService(mock_client)

@pytest.mark.asyncio
async def test_get_board(board_service, mock_client):
    board_id = "board123"
    mock_data = {"id": board_id, "name": "Test Board", "url": "http://trello.com/b/123"}
    mock_client.GET.return_value = mock_data

    board = await board_service.get_board(board_id)

    assert isinstance(board, TrelloBoard)
    assert board.id == board_id
    assert board.name == "Test Board"
    mock_client.GET.assert_called_once_with(f"/boards/{board_id}")

@pytest.mark.asyncio
async def test_get_boards(board_service, mock_client):
    mock_data = [
        {"id": "board1", "name": "Board 1", "url": "http://trello.com/b/1"},
        {"id": "board2", "name": "Board 2", "url": "http://trello.com/b/2"}
    ]
    mock_client.GET.return_value = mock_data

    boards = await board_service.get_boards()

    assert len(boards) == 2
    assert isinstance(boards[0], TrelloBoard)
    assert boards[0].id == "board1"
    mock_client.GET.assert_called_once_with("/members/me/boards")

@pytest.mark.asyncio
async def test_get_boards_specific_member(board_service, mock_client):
    member_id = "user123"
    mock_client.GET.return_value = []

    await board_service.get_boards(member_id)

    mock_client.GET.assert_called_once_with(f"/members/{member_id}/boards")
