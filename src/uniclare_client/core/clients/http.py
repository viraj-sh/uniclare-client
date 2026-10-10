import http.cookiejar

import httpx


class NullCookieJar(http.cookiejar.CookieJar):
    def set_cookie(self, cookie, *args, **kwargs):
        pass

    def extract_cookies(self, response, request, *args, **kwargs):
        pass


class HTTPClientState:
    client: httpx.AsyncClient | None = None


http_state = HTTPClientState()


async def init_http_client():
    if http_state.client is not None:
        return

    http_state.client = httpx.AsyncClient(
        cookies=NullCookieJar(),
        timeout=httpx.Timeout(connect=10.0, read=120.0, write=120.0, pool=30.0),
        limits=httpx.Limits(
            max_connections=100, max_keepalive_connections=20, keepalive_expiry=120.0
        ),
        follow_redirects=True,
    )


async def get_http_client():
    if http_state.client is None:
        raise RuntimeError("HTTP Client not initialized")
    return http_state.client


async def close_http_client():
    if http_state.client is None:
        return
    await http_state.client.aclose()
    http_state.client = None
