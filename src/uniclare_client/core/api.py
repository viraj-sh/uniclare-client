from contextlib import AsyncExitStack

from uniclare_client.core import lifecycle
from uniclare_client.core.config import Settings


class App:
    def __init__(self, config: Settings | None = None) -> None:
        self.config = config or Settings()
        self._stack = AsyncExitStack()
        self._started = False

    async def start(self) -> "App":
        if self._started:
            return self
        try:
            res = await lifecycle.start(self.config, self._stack)
        except BaseException:
            await self._stack.aclose()
            raise
        self._http = res.http
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
