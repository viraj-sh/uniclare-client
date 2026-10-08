import httpx

from app.clients.http import get_http_client
from app.notifications.endpoints import noti as notification
from app.notifications.parsers import parse_noti
from app.notifications.schemas import NotificationResponse


async def noti(session_token: str) -> list[NotificationResponse]:
    client = await get_http_client()
    try:
        response = await notification(session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_noti(response)
