import httpx

from app.clients.http import get_http_client
from app.profile.endpoints import profile as prf
from app.profile.parsers import parse_profile
from app.profile.schemas import ProfileResult


async def profile(session_token: str) -> ProfileResult:
    client = await get_http_client()
    try:
        response = await prf(session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_profile(response)
