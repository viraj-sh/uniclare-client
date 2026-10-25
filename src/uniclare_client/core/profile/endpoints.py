import httpx

from uniclare_client.core.clients.http import HttpClient
from uniclare_client.core.constants import MAIN_REFERER, build_headers
from uniclare_client.core.profile.constants import PROFILE_PATH


async def profile(http: HttpClient, session_token: str) -> httpx.Response:
    return await http.request(
        "GET",
        PROFILE_PATH,
        headers=build_headers(
            base_url=http.base_url,
            session_token=session_token,
            referer_path=MAIN_REFERER,
        ),
    )
