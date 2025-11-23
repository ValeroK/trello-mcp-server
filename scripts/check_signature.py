import inspect
from mcp.server.fastmcp import Context
from server.utils.decorators import mcp_tool

@mcp_tool
async def test_func(context: Context, my_arg: str, my_int: int = 1):
    pass

sig = inspect.signature(test_func)
print(f"Signature: {sig}")

parameters = list(sig.parameters.values())
print(f"Parameters: {[p.name for p in parameters]}")

if 'my_arg' not in sig.parameters:
    print("FAIL: 'my_arg' not found in signature")
else:
    print("PASS: 'my_arg' found in signature")
