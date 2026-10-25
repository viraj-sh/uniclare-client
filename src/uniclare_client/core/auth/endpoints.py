import httpx

from uniclare_client.core.auth.constants import (
    CAPTCHA_PATH,
    OTP_PATH,
    RESET_PASS_PATH,
    SIGNIN_PATH,
    SIGNOUT_PATH,
    VERIFY_SESSION_PARAMS,
    VERIFY_SESSION_PATH,
)
from uniclare_client.core.clients.http import HttpClient
from uniclare_client.core.constants import INDEX_REFERER, MAIN_REFERER, build_headers


async def captcha(http: HttpClient) -> httpx.Response:
    return await http.request(
        "GET",
        CAPTCHA_PATH,
        headers=build_headers(base_url=http.base_url),
    )


async def signin(
    http: HttpClient,
    *,
    reg_no: str,
    password: str,
    captcha_code: int,
    session_token: str,
) -> httpx.Response:
    return await http.request(
        "POST",
        SIGNIN_PATH,
        data={"regno": reg_no, "passwd": password, "captcha": captcha_code},
        headers=build_headers(
            base_url=http.base_url,
            session_token=session_token,
            referer_path=MAIN_REFERER,
        ),
        idempotent=False,
    )


async def verify_session(http: HttpClient, session_token: str) -> httpx.Response:
    return await http.request(
        "GET",
        VERIFY_SESSION_PATH,
        params=VERIFY_SESSION_PARAMS,
        headers=build_headers(
            base_url=http.base_url,
            session_token=session_token,
            referer_path=MAIN_REFERER,
        ),
    )


async def signout(http: HttpClient, session_token: str) -> httpx.Response:
    return await http.request(
        "POST",
        SIGNOUT_PATH,
        headers=build_headers(
            base_url=http.base_url,
            session_token=session_token,
            referer_path=MAIN_REFERER,
        ),
        idempotent=False,
    )


async def request_otp(
    http: HttpClient,
    *,
    mobile_no: str,
) -> httpx.Response:
    return await http.request(
        "POST",
        OTP_PATH,
        data={"mobile": mobile_no},
        headers=build_headers(
            base_url=http.base_url,
            referer_path=INDEX_REFERER,
            form_post=True,
        ),
        idempotent=False,
    )


async def reset_password(
    http: HttpClient,
    *,
    mobile_no: str,
    otp_code: str,
    new_password: str,
    session_token: str,
) -> httpx.Response:
    return await http.request(
        "POST",
        RESET_PASS_PATH,
        data={"mobile": mobile_no, "otp": otp_code, "password": new_password},
        headers=build_headers(
            base_url=http.base_url,
            session_token=session_token,
            referer_path=MAIN_REFERER,
        ),
        idempotent=False,
    )
