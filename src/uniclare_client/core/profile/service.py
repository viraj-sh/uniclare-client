import httpx

from uniclare_client.core.clients.http import get_http_client
from uniclare_client.core.profile.endpoints import profile as prf
from uniclare_client.core.profile.parsers import parse_profile
from uniclare_client.core.profile.schemas import ProfileResult


async def profile(session_token: str) -> ProfileResult:
    client = await get_http_client()
    try:
        response = await prf(session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_profile(response)
