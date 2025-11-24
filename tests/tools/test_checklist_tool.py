import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.server.fastmcp import Context
from server.tools.checklist import (
    get_checklist, get_card_checklists, create_checklist, update_checklist, 
    delete_checklist, add_checkitem, update_checkitem, delete_checkitem
)

@pytest.fixture
def mock_context():
    return MagicMock(spec=Context)

@pytest.fixture
def mock_service(mocker):
    return mocker.patch("server.tools.checklist.service", autospec=True)

@pytest.mark.asyncio
async def test_get_checklist_tool(mock_context, mock_service):
    checklist_id = "chk1"
    expected_data = {"id": checklist_id, "name": "Checklist"}
    mock_service.get_checklist.return_value = expected_data

    result = await get_checklist(mock_context, checklist_id)

    assert result == expected_data
    mock_service.get_checklist.assert_called_once_with(checklist_id)

@pytest.mark.asyncio
async def test_get_card_checklists_tool(mock_context, mock_service):
    card_id = "c1"
    expected_data = [{"id": "chk1", "name": "Checklist"}]
    mock_service.get_card_checklists.return_value = expected_data

    result = await get_card_checklists(mock_context, card_id)

    assert result == expected_data
    mock_service.get_card_checklists.assert_called_once_with(card_id)

@pytest.mark.asyncio
async def test_create_checklist_tool(mock_context, mock_service):
    card_id = "c1"
    name = "New Checklist"
    expected_data = {"id": "chk1", "name": name, "idCard": card_id}
    mock_service.create_checklist.return_value = expected_data

    result = await create_checklist(mock_context, card_id, name)

    assert result == expected_data
    mock_service.create_checklist.assert_called_once_with(card_id, name, None)

@pytest.mark.asyncio
async def test_update_checklist_tool(mock_context, mock_service):
    checklist_id = "chk1"
    name = "Updated Name"
    expected_data = {"id": checklist_id, "name": name}
    mock_service.update_checklist.return_value = expected_data

    result = await update_checklist(mock_context, checklist_id, name=name)

    assert result == expected_data
    mock_service.update_checklist.assert_called_once_with(checklist_id, name, None)

@pytest.mark.asyncio
async def test_delete_checklist_tool(mock_context, mock_service):
    checklist_id = "chk1"
    expected_data = {}
    mock_service.delete_checklist.return_value = expected_data

    result = await delete_checklist(mock_context, checklist_id)

    assert result == expected_data
    mock_service.delete_checklist.assert_called_once_with(checklist_id)

@pytest.mark.asyncio
async def test_add_checkitem_tool(mock_context, mock_service):
    checklist_id = "chk1"
    name = "Item 1"
    expected_data = {"id": "item1", "name": name, "state": "incomplete"}
    mock_service.add_checkitem.return_value = expected_data

    result = await add_checkitem(mock_context, checklist_id, name)

    assert result == expected_data
    mock_service.add_checkitem.assert_called_once_with(checklist_id, name, False, None)

@pytest.mark.asyncio
async def test_update_checkitem_tool(mock_context, mock_service):
    checklist_id = "chk1"
    checkitem_id = "item1"
    expected_data = {"id": checkitem_id, "state": "complete"}
    mock_service.update_checkitem.return_value = expected_data

    result = await update_checkitem(mock_context, checklist_id, checkitem_id, checked=True)

    assert result == expected_data
    mock_service.update_checkitem.assert_called_once_with(checklist_id, checkitem_id, None, True, None)

@pytest.mark.asyncio
async def test_delete_checkitem_tool(mock_context, mock_service):
    checklist_id = "chk1"
    checkitem_id = "item1"
    expected_data = {}
    mock_service.delete_checkitem.return_value = expected_data

    result = await delete_checkitem(mock_context, checklist_id, checkitem_id)

    assert result == expected_data
    mock_service.delete_checkitem.assert_called_once_with(checklist_id, checkitem_id)
