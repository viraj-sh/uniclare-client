from contextlib import AsyncExitStack

from uniclare_client.core import lifecycle
from uniclare_client.core.auth import AuthService
from uniclare_client.core.config import Settings
from uniclare_client.core.errors import AppNotStarted
from uniclare_client.core.profile import ProfileService
from uniclare_client.core.results import ResultsService


class App:
    def __init__(self, config: Settings | None = None) -> None:
        self.config = config or Settings()
        self._stack = AsyncExitStack()
        self._started = False
        self._auth: AuthService | None = None
        self._results: ResultsService | None = None
        self._profile: ProfileService | None = None

    @property
    def auth(self) -> AuthService:
        if not self._started or self._auth is None:
            raise AppNotStarted("App not started")
        return self._auth

    @property
    def results(self) -> ResultsService:
        if not self._started or self._results is None:
            raise AppNotStarted("App not started")
        return self._results

    @property
    def profile(self) -> ProfileService:
        if not self._started or self._profile is None:
            raise AppNotStarted("App not started")
        return self._profile

    async def start(self) -> "App":
        if self._started:
            return self
        try:
            res = await lifecycle.start(self.config, self._stack)
        except BaseException:
            await self._stack.aclose()
            raise
        self._http = res.http
        self._auth = AuthService(res.http)
        self._results = ResultsService(res.http)
        self._profile = ProfileService(res.http)
        self._started = True
        return self

    async def close(self) -> None:
        if self._started:
            self._started = False
            await self._stack.aclose()

    async def __aenter__(self) -> "App":
        return await self.start()

    async def __aexit__(self, *exc_info) -> None:
        await self.close()

    async def health(self) -> dict[str, bool]:
        http_ok = self._started and self._http.is_started
        return {"http": http_ok}
