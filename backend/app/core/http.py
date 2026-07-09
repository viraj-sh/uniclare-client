import http.cookiejar
from typing import Annotated

import httpx
from fastapi import Depends
from fastapi.security import HTTPBearer

security = HTTPBearer()


class NullCookieJar(http.cookiejar.CookieJar):
    def set_cookie(self, cookie, *args, **kwargs):
        pass

    def extract_cookies(self, response, request, *args, **kwargs):
        pass


class HTTPClientState:
    client: httpx.AsyncClient | None = None


http_state = HTTPClientState()


async def get_http_client():
    if http_state.client is None:
        raise RuntimeError("HTTP client not initialized")
    return http_state.client


HTTPClientDep = Annotated[httpx.AsyncClient, Depends(get_http_client)]
