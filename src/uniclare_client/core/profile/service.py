from uniclare_client.core.clients.http import HttpClient
from uniclare_client.core.profile import endpoints, parsers
from uniclare_client.core.profile.schema import Profile


class ProfileService:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def get(self, session_token: str) -> Profile:
        return parsers.parse_profile(await endpoints.profile(self._http, session_token))
