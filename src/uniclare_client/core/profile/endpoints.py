import httpx

from uniclare_client.core.constants import API_BASE_URL
from uniclare_client.core.http_headers import authenticated_headers

PROFILE_URL = f"{API_BASE_URL}/src/profile.php"


async def profile(session_token: str, client: httpx.AsyncClient):
    return await client.get(
        url=PROFILE_URL, headers=authenticated_headers(session_token)
    )
