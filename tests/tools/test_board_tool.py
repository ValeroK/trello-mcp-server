import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.server.fastmcp import Context
from server.tools.board import get_board, get_boards
from server.models import TrelloBoard

@pytest.fixture
def mock_context():
    return MagicMock(spec=Context)

@pytest.fixture
def mock_service(mocker):
    return mocker.patch("server.tools.board.service", autospec=True)

@pytest.mark.asyncio
async def test_get_board_tool(mock_context, mock_service):
    board_id = "board123"
    expected_board = TrelloBoard(id=board_id, name="Test Board", url="http://test.com")
    mock_service.get_board.return_value = expected_board

    result = await get_board(mock_context, board_id)

    assert result == expected_board
    mock_service.get_board.assert_called_once_with(board_id)

@pytest.mark.asyncio
async def test_get_boards_tool(mock_context, mock_service):
    expected_boards = [TrelloBoard(id="b1", name="B1", url="u1")]
    mock_service.get_boards.return_value = expected_boards

    result = await get_boards(mock_context)

    assert result == expected_boards
    mock_service.get_boards.assert_called_once()
