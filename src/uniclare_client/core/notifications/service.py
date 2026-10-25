from uniclare_client.core.clients.http import HttpClient
from uniclare_client.core.notifications import endpoints, parsers
from uniclare_client.core.notifications.schema import Notification


class NotificationsService:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def list(self, session_token: str) -> list[Notification]:
        return parsers.parse_notifications(
            await endpoints.list_notifications(self._http, session_token)
        )
