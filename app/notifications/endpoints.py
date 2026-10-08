import httpx

from app.constants import API_BASE_URL
from app.http_headers import authenticated_headers


async def noti(session_token: str, client: httpx.AsyncClient):
    return await client.get(
        url=f"{API_BASE_URL}/src/notificationstatus.php",
        headers=authenticated_headers(session_token),
    )
