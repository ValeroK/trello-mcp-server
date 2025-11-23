import asyncio
import logging
import os
from unittest.mock import AsyncMock

from dotenv import load_dotenv
from mcp.server.fastmcp import Context

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the tool to verify
# We need to make sure the server module is in the path
import sys
sys.path.append(os.getcwd())

from server.tools.board import get_boards

async def verify():
    print("Verifying get_boards tool...")
    
    # Mock the context
    mock_context = AsyncMock(spec=Context)
    mock_context.error = AsyncMock()
    
    try:
        # Call the tool
        # The decorator expects (context, *args, **kwargs)
        # But fastmcp injects context. When calling directly, we must provide it if the function signature has it.
        # Our refactored functions have (context: Context, ...)
        
        boards = await get_boards(mock_context)
        
        print(f"Successfully retrieved {len(boards)} boards.")
        for board in boards[:3]:
            print(f" - {board.name} ({board.id})")
            
        print("\nVerification Successful!")
        
    except Exception as e:
        print(f"\nVerification Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify())
