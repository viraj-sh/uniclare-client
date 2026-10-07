import httpx

from app.auth.endpoints import captcha, signin, signout
from app.auth.endpoints import verify_session as verify_sess
from app.auth.parsers import (
    parse_captcha,
    parse_signin,
    parse_signout,
    parse_verify_session,
)
from app.auth.schemas import (
    CaptchaResult,
    SigninResult,
    SignoutResult,
    VerifySessionResult,
)
from app.clients.http import get_http_client


async def login(
    mobile_no: str, password: str, captcha: int, session_token: str
) -> SigninResult:
    client = await get_http_client()
    try:
        response = await signin(mobile_no, password, captcha, session_token, client)
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


async def verify_session(session_token: str) -> VerifySessionResult:
    client = await get_http_client()
    try:
        response = await verify_sess(session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_verify_session(response)


async def logout(session_token: str) -> SignoutResult:
    client = await get_http_client()
    try:
        response = await signout(session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_signout(response)
