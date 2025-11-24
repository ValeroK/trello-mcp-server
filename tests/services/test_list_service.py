import pytest
from unittest.mock import AsyncMock
from server.services.list import ListService
from server.models import TrelloList

@pytest.fixture
def mock_client():
    return AsyncMock()

@pytest.fixture
def list_service(mock_client):
    return ListService(mock_client)

@pytest.mark.asyncio
async def test_get_list(list_service, mock_client):
    list_id = "list123"
    mock_data = {
        "id": list_id, 
        "name": "Test List", 
        "idBoard": "board1", 
        "pos": 100.0
    }
    mock_client.GET.return_value = mock_data

    trello_list = await list_service.get_list(list_id)

    assert isinstance(trello_list, TrelloList)
    assert trello_list.id == list_id
    assert trello_list.name == "Test List"
    mock_client.GET.assert_called_once_with(f"/lists/{list_id}")

@pytest.mark.asyncio
async def test_get_lists(list_service, mock_client):
    board_id = "board123"
    mock_data = [
        {"id": "list1", "name": "List 1", "idBoard": board_id, "pos": 100.0},
        {"id": "list2", "name": "List 2", "idBoard": board_id, "pos": 200.0}
    ]
    mock_client.GET.return_value = mock_data

    lists = await list_service.get_lists(board_id)

    assert len(lists) == 2
    assert isinstance(lists[0], TrelloList)
    assert lists[0].id == "list1"
    mock_client.GET.assert_called_once_with(f"/boards/{board_id}/lists")

@pytest.mark.asyncio
async def test_create_list(list_service, mock_client):
    board_id = "board123"
    name = "New List"
    mock_data = {
        "id": "newlist", 
        "name": name, 
        "idBoard": board_id, 
        "pos": 300.0
    }
    mock_client.POST.return_value = mock_data

    new_list = await list_service.create_list(board_id, name)

    assert isinstance(new_list, TrelloList)
    assert new_list.name == name
    mock_client.POST.assert_called_once_with("/lists", data={"name": name, "idBoard": board_id, "pos": "bottom"})

@pytest.mark.asyncio
async def test_update_list(list_service, mock_client):
    list_id = "list123"
    new_name = "Updated List"
    mock_data = {
        "id": list_id, 
        "name": new_name, 
        "idBoard": "board1", 
        "pos": 100.0
    }
    mock_client.PUT.return_value = mock_data

    updated_list = await list_service.update_list(list_id, new_name)

    assert updated_list.name == new_name
    mock_client.PUT.assert_called_once_with(f"/lists/{list_id}", data={"name": new_name})

@pytest.mark.asyncio
async def test_delete_list(list_service, mock_client):
    list_id = "list123"
    mock_data = {
        "id": list_id, 
        "name": "List 1",
        "idBoard": "board1",
        "pos": 100.0,
        "closed": True
    }
    mock_client.PUT.return_value = mock_data

    archived_list = await list_service.delete_list(list_id)

    assert archived_list.closed is True
    mock_client.PUT.assert_called_once_with(f"/lists/{list_id}/closed", data={"value": "true"})
