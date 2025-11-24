import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.server.fastmcp import Context
from server.tools.list import get_list, get_lists, create_list, update_list, delete_list
from server.models import TrelloList

@pytest.fixture
def mock_context():
    return MagicMock(spec=Context)

@pytest.fixture
def mock_service(mocker):
    return mocker.patch("server.tools.list.service", autospec=True)

@pytest.mark.asyncio
async def test_get_list_tool(mock_context, mock_service):
    list_id = "list123"
    expected_list = TrelloList(
        id=list_id, 
        name="Test List", 
        idBoard="b1", 
        pos=1.0
    )
    mock_service.get_list.return_value = expected_list

    result = await get_list(mock_context, list_id)

    assert result == expected_list
    mock_service.get_list.assert_called_once_with(list_id)

@pytest.mark.asyncio
async def test_get_lists_tool(mock_context, mock_service):
    board_id = "b1"
    expected_lists = [
        TrelloList(
            id="l1", 
            name="L1", 
            idBoard=board_id, 
            pos=1.0
        )
    ]
    mock_service.get_lists.return_value = expected_lists

    result = await get_lists(mock_context, board_id)

    assert result == expected_lists
    mock_service.get_lists.assert_called_once_with(board_id)

@pytest.mark.asyncio
async def test_create_list_tool(mock_context, mock_service):
    board_id = "b1"
    name = "New List"
    expected_list = TrelloList(
        id="l1", 
        name=name, 
        idBoard=board_id, 
        pos=1.0
    )
    mock_service.create_list.return_value = expected_list

    result = await create_list(mock_context, board_id, name)

    assert result == expected_list
    mock_service.create_list.assert_called_once_with(board_id, name, "bottom")

@pytest.mark.asyncio
async def test_update_list_tool(mock_context, mock_service):
    list_id = "l1"
    name = "Updated List"
    expected_list = TrelloList(
        id=list_id, 
        name=name, 
        idBoard="b1", 
        pos=1.0
    )
    mock_service.update_list.return_value = expected_list

    result = await update_list(mock_context, list_id, name)

    assert result == expected_list
    mock_service.update_list.assert_called_once_with(list_id, name)

@pytest.mark.asyncio
async def test_delete_list_tool(mock_context, mock_service):
    list_id = "l1"
    expected_list = TrelloList(
        id=list_id, 
        name="L1", 
        idBoard="b1", 
        closed=True, 
        pos=1.0
    )
    mock_service.delete_list.return_value = expected_list

    result = await delete_list(mock_context, list_id)

    assert result == expected_list
    mock_service.delete_list.assert_called_once_with(list_id)
