from server.mcp_instance import mcp
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
import httpx

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    # Check for required environment variables
    # Note: Settings validation ensures these exist at startup, but we check here for completeness
    from server.config import settings
    
    if not settings.TRELLO_API_KEY or not settings.TRELLO_TOKEN:
        return JSONResponse(
            {"status": "unhealthy", "reason": "Missing Trello credentials"},
            status_code=HTTP_503_SERVICE_UNAVAILABLE
        )
    # Check Trello API connectivity
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.trello.com/1/members/me",
                params={
                    "key": settings.TRELLO_API_KEY,
                    "token": settings.TRELLO_TOKEN
                },
                timeout=5.0
            )
            response.raise_for_status()
    except Exception as e:
        return JSONResponse(
            {"status": "unhealthy", "reason": f"Trello API error: {str(e)}"},
            status_code=HTTP_503_SERVICE_UNAVAILABLE
        )
    return JSONResponse({"status": "healthy", "trello_connection": "ok", "version": "1.0.0"}) 