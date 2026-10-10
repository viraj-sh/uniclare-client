import httpx

from uniclare_client.core.clients.http import get_http_client
from uniclare_client.core.notifications.endpoints import noti as notification
from uniclare_client.core.notifications.parsers import parse_noti
from uniclare_client.core.notifications.schemas import NotificationResponse


async def noti(session_token: str) -> list[NotificationResponse]:
    client = await get_http_client()
    try:
        response = await notification(session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_noti(response)
