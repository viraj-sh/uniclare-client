import httpx

from app.auth.endpoints import captcha, signin
from app.auth.parsers import parse_captcha, parse_signin
from app.auth.schemas import CaptchaResult, SigninResult
from app.clients.http import get_http_client


async def login(
    mobile_no: str, password: str, captcha: int, session_id: str
) -> SigninResult:
    client = await get_http_client()
    try:
        response = await signin(mobile_no, password, captcha, session_id, client)
    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_signin(response)


async def get_captcha() -> CaptchaResult:
    client = await get_http_client()
    try:
        response = await captcha(client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_captcha(response)
