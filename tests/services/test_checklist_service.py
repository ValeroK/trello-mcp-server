import pytest
from unittest.mock import AsyncMock
from server.services.checklist import ChecklistService

@pytest.fixture
def mock_client():
    return AsyncMock()

@pytest.fixture
def checklist_service(mock_client):
    return ChecklistService(mock_client)

@pytest.mark.asyncio
async def test_get_checklist(checklist_service, mock_client):
    checklist_id = "chk123"
    mock_data = {"id": checklist_id, "name": "Test Checklist"}
    mock_client.GET.return_value = mock_data

    checklist = await checklist_service.get_checklist(checklist_id)

    assert checklist == mock_data
    mock_client.GET.assert_called_once_with(f"/checklists/{checklist_id}")

@pytest.mark.asyncio
async def test_get_card_checklists(checklist_service, mock_client):
    card_id = "card123"
    mock_data = [{"id": "chk1", "name": "Checklist 1"}]
    mock_client.GET.return_value = mock_data

    checklists = await checklist_service.get_card_checklists(card_id)

    assert checklists == mock_data
    mock_client.GET.assert_called_once_with(f"/cards/{card_id}/checklists")

@pytest.mark.asyncio
async def test_create_checklist(checklist_service, mock_client):
    card_id = "card123"
    name = "New Checklist"
    mock_data = {"id": "newchk", "name": name, "idCard": card_id}
    mock_client.POST.return_value = mock_data

    checklist = await checklist_service.create_checklist(card_id, name)

    assert checklist == mock_data
    mock_client.POST.assert_called_once_with("/checklists", data={"idCard": card_id, "name": name})

@pytest.mark.asyncio
async def test_update_checklist(checklist_service, mock_client):
    checklist_id = "chk123"
    name = "Updated Checklist"
    mock_data = {"id": checklist_id, "name": name}
    mock_client.PUT.return_value = mock_data

    checklist = await checklist_service.update_checklist(checklist_id, name=name)

    assert checklist == mock_data
    mock_client.PUT.assert_called_once_with(f"/checklists/{checklist_id}", data={"name": name})

@pytest.mark.asyncio
async def test_delete_checklist(checklist_service, mock_client):
    checklist_id = "chk123"
    mock_data = {"limits": {}}
    mock_client.DELETE.return_value = mock_data

    response = await checklist_service.delete_checklist(checklist_id)

    assert response == mock_data
    mock_client.DELETE.assert_called_once_with(f"/checklists/{checklist_id}")

@pytest.mark.asyncio
async def test_add_checkitem(checklist_service, mock_client):
    checklist_id = "chk123"
    name = "Item 1"
    mock_data = {"id": "item1", "name": name, "state": "incomplete"}
    mock_client.POST.return_value = mock_data

    item = await checklist_service.add_checkitem(checklist_id, name)

    assert item == mock_data
    mock_client.POST.assert_called_once_with(f"/checklists/{checklist_id}/checkItems", data={"name": name, "checked": False})

@pytest.mark.asyncio
async def test_update_checkitem(checklist_service, mock_client):
    checklist_id = "chk123"
    checkitem_id = "item1"
    mock_data = {"id": checkitem_id, "state": "complete"}
    mock_client.PUT.return_value = mock_data

    item = await checklist_service.update_checkitem(checklist_id, checkitem_id, checked=True)

    assert item == mock_data
    mock_client.PUT.assert_called_once_with(f"/checklists/{checklist_id}/checkItems/{checkitem_id}", data={"checked": True})

@pytest.mark.asyncio
async def test_delete_checkitem(checklist_service, mock_client):
    checklist_id = "chk123"
    checkitem_id = "item1"
    mock_data = {}
    mock_client.DELETE.return_value = mock_data

    response = await checklist_service.delete_checkitem(checklist_id, checkitem_id)

    assert response == mock_data
    mock_client.DELETE.assert_called_once_with(f"/checklists/{checklist_id}/checkItems/{checkitem_id}")
