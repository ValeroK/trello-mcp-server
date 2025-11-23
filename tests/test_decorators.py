import pytest
from server.utils.decorators import mcp_tool

@pytest.mark.asyncio
async def test_mcp_tool_success(mock_context, mock_logger):
    @mcp_tool
    async def sample_tool(context, arg1, arg2):
        return f"Success: {arg1} {arg2}"

    result = await sample_tool(mock_context, "hello", "world")

    assert result == "Success: hello world"
    # Verify logging
    assert mock_logger.info.call_count == 2
    mock_logger.info.assert_any_call("Starting sample_tool with args: ('hello', 'world') kwargs: {}")
    mock_logger.info.assert_any_call("Successfully completed sample_tool")

@pytest.mark.asyncio
async def test_mcp_tool_exception(mock_context, mock_logger):
    @mcp_tool
    async def failing_tool(context):
        raise ValueError("Something went wrong")

    with pytest.raises(ValueError, match="Something went wrong"):
        await failing_tool(mock_context)

    # Verify error logging and context error
    mock_logger.error.assert_called_once()
    mock_context.error.assert_called_once()
    
    # Check that the error message contains the exception message
    error_log = mock_logger.error.call_args[0][0]
    assert "Failed to execute failing_tool: Something went wrong" in error_log
    assert "Traceback" in error_log
