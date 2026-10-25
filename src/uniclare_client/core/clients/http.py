import asyncio
import http.cookiejar
import random
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from uniclare_client.core.config import Settings
from uniclare_client.core.errors import (
    AppNotStarted,
    ExternalTimeout,
    ExternalUnavailable,
    InvalidResponse,
    RateLimited,
)

T = TypeVar("T", bound=BaseModel)

RETRY_STATUS = {429, 502, 503, 504}
SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
MAX_BACKOFF = 8.0


def _backoff(attempt: int, response: httpx.Response | None = None) -> float:
    if response is not None:
        retry_after = response.headers.get("Retry-After", "")
        if retry_after.isdigit():
            return min(float(retry_after), MAX_BACKOFF)
    return min(MAX_BACKOFF, 0.5 * 2 ** (attempt - 1)) * random.uniform(0.5, 1.5)


class NullCookieJar(http.cookiejar.CookieJar):
    def set_cookie(self, cookie, *args, **kwargs):
        pass

    def extract_cookies(self, response, request, *args, **kwargs):
        pass


class HttpClient:
    def __init__(self, config: Settings) -> None:
        self._config = config
        self._client: httpx.AsyncClient | None = None

    @property
    def is_started(self) -> bool:
        return self._client is not None

    async def _send(
        self, client: httpx.AsyncClient, method: str, url: str, **kwargs: Any
    ) -> httpx.Response:
        try:
            return await client.request(method, url, **kwargs)
        except httpx.TimeoutException as exc:
            raise ExternalTimeout("Uniclare request timed out") from exc
        except httpx.TransportError as exc:
            raise ExternalUnavailable("Could not reach Uniclare") from exc

    async def start(self) -> None:
        if self._client is not None:
            return
        self._client = httpx.AsyncClient(
            base_url=self._config.base_url,
            cookies=NullCookieJar(),
            timeout=httpx.Timeout(
                connect=self._config.http_connect_timeout,
                read=self._config.http_read_timeout,
                write=self._config.http_write_timeout,
                pool=self._config.http_pool_timeout,
            ),
            limits=httpx.Limits(
                max_connections=self._config.http_max_connections,
                max_keepalive_connections=self._config.http_max_keepalive,
                keepalive_expiry=self._config.http_keepalive_expiry,
            ),
            follow_redirects=True,
        )

    async def close(self) -> None:
        if self._client is None:
            return
        await self._client.aclose()
        self._client = None

    async def request(
        self,
        method: str,
        url: str,
        *,
        idempotent: bool | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        client = self._client
        if client is None:
            raise AppNotStarted("HttpClient not started")

        if idempotent is None:
            idempotent = method.upper() in SAFE_METHODS
        max_attempts = (self._config.http_retries if idempotent else 0) + 1

        attempt = 0
        while True:
            attempt += 1
            final = attempt >= max_attempts
            try:
                response = await self._send(client, method, url, **kwargs)
            except (ExternalTimeout, ExternalUnavailable):
                if final:
                    raise
                delay = _backoff(attempt)
            else:
                if response.status_code not in RETRY_STATUS:
                    return response
                if final:
                    if response.status_code == 429:
                        raise RateLimited("Uniclare rate limit exceeded")
                    return response
                delay = _backoff(attempt, response)
            await asyncio.sleep(delay)


def read_json(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError as exc:
        raise InvalidResponse(
            f"Response was not JSON (HTTP {response.status_code})"
        ) from exc


def read_model(response: httpx.Response, model: type[T]) -> T:
    data = read_json(response)
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise InvalidResponse(
            f"{model.__name__}: response format changed",
            details={"errors": exc.errors(include_url=False, include_input=False)},
        ) from exc
