import httpx

from app.constants import API_BASE_URL
from app.http_headers import authenticated_headers, unauthenticated_headers

SIGNIN_URL = f"{API_BASE_URL}/signin.php"
CAPTCHA_URL = f"{API_BASE_URL}/get_captcha.php"
VERIFY_SESSION_URL = f"{API_BASE_URL}/app.php"
SIGNOUT_URL = f"{API_BASE_URL}/src/logout.php"
OTP_URL = f"{API_BASE_URL}/forgot-password.php"
RESET_PASS_URL = f"{API_BASE_URL}/resetpassword.php"
VERIFY_PASS_URL = f"{API_BASE_URL}/src/chngPassword.php"


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


async def signout(session_token: str, client: httpx.AsyncClient):
    return await client.post(
        url=SIGNOUT_URL, headers=authenticated_headers(session_token)
    )


async def otp(
    mob_no: str,
    session_token: str,
    client: httpx.AsyncClient,
):
    payload = {"mobile": mob_no}
    return await client.post(
        url=OTP_URL,
        data=payload,
        headers=unauthenticated_headers(),
    )


async def reset_password(
    mob_no: str,
    otp: str,
    new_password: str,
    session_token: str,
    client: httpx.AsyncClient,
):
    payload = {"mobile": mob_no, "otp": otp, "password": new_password}
    return await client.post(
        url=RESET_PASS_URL,
        data=payload,
        headers=authenticated_headers(session_token),
    )
