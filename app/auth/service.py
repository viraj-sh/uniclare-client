import httpx

from app.auth.endpoints import (
    captcha,
    otp,
    reset_password,
    signin,
    signout,
)
from app.auth.endpoints import verify_session as verify_sess
from app.auth.parsers import (
    parse_captcha,
    parse_otp,
    parse_reset_password,
    parse_signin,
    parse_signout,
    parse_verify_session,
)
from app.auth.schemas import (
    CaptchaResult,
    OTPResult,
    ResetPassResult,
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


async def get_otp(mobile_no: str, session_token: str) -> OTPResult:
    client = await get_http_client()
    try:
        response = await otp(mobile_no, session_token, client)
    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_otp(response)


async def reset_pass(
    mob_no: str,
    otp: str,
    new_password: str,
    session_token: str,
) -> ResetPassResult:
    client = await get_http_client()
    try:
        response = await reset_password(
            mob_no, otp, new_password, session_token, client
        )
    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")
    return parse_reset_password(response)
