import httpx

from app.constants import API_BASE_URL
from app.http_headers import authenticated_headers, unauthenticated_headers

SIGNIN_URL = f"{API_BASE_URL}/signin.php"
CAPTCHA_URL = f"{API_BASE_URL}/get_captcha.php"
VERIFY_SESSION_URL = f"{API_BASE_URL}/app.php"


async def signin(
    mob_no: str,
    password: str,
    captcha: int,
    session_token: str,
    client: httpx.AsyncClient,
):
    payload = {"regno": mob_no, "passwd": password, "captcha": captcha}
    return await client.post(
        url=SIGNIN_URL,
        data=payload,
        headers=authenticated_headers(session_token),
    )


async def captcha(client: httpx.AsyncClient):
    return await client.get(url=CAPTCHA_URL, headers=unauthenticated_headers())


async def verify_session(session_token: str, client: httpx.AsyncClient):
    return await client.get(
        url=VERIFY_SESSION_URL,
        headers=authenticated_headers(session_token),
        params={"a": "showneedhelp", "univcode": "undefined", "fregno": "undefined"},
    )
