import httpx

from app.constants import API_BASE_URL
from app.http_headers import authenticated_headers, unauthenticated_headers

SIGNIN_URL = f"{API_BASE_URL}/signin.php"
CAPTCHA_URL = f"{API_BASE_URL}/get_captcha.php"


async def signin(
    mob_no: str, password: str, captcha: int, session_id: str, client: httpx.AsyncClient
):
    payload = {"regno": mob_no, "passwd": password, "captcha": captcha}
    return await client.post(
        url=SIGNIN_URL,
        data=payload,
        headers=authenticated_headers(session_id),
    )


async def captcha(client: httpx.AsyncClient):
    return await client.get(url=CAPTCHA_URL, headers=unauthenticated_headers())
