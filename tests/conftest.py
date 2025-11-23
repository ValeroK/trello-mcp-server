import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.server.fastmcp import Context

@pytest.fixture
def mock_context():
    context = AsyncMock(spec=Context)
    context.error = AsyncMock()
    return context

@pytest.fixture
def mock_logger():
    with pytest.MonkeyPatch.context() as m:
        logger = MagicMock()
        m.setattr("server.utils.decorators.logger", logger)
        yield logger
