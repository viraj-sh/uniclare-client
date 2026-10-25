import httpx

from uniclare_client.core.auth.schema import Captcha, OtpInfo, Session
from uniclare_client.core.clients.http import read_json
from uniclare_client.core.errors import (
    InvalidCredentials,
    InvalidInput,
    InvalidResponse,
)


def _phpsessid(response: httpx.Response) -> str | None:
    token = response.cookies.get("PHPSESSID")
    if token:
        return token
    for header in response.headers.get_list("set-cookie"):
        if header.startswith("PHPSESSID="):
            return header.split(";", 1)[0].removeprefix("PHPSESSID=")
    return None


def parse_captcha(response: httpx.Response) -> Captcha:
    if response.status_code != 200:
        raise InvalidResponse(f"Captcha: unexpected status {response.status_code}")

    data = read_json(response)
    raw = data.get("captcha")
    if raw is None:
        raise InvalidResponse("Captcha: missing 'captcha' field")
    try:
        value = int(raw)
    except (TypeError, ValueError):
        raise InvalidResponse("Captcha: 'captcha' field is not an integer")

    token = _phpsessid(response)
    if not token:
        raise InvalidResponse("Captcha: no PHPSESSID returned")

    return Captcha(value=value, session_token=token)


def _error_code(data: dict) -> int:
    raw = data.get("error_code", 0)
    try:
        return int(raw)
    except (TypeError, ValueError):
        raise InvalidResponse(f"non-integer error_code: {raw!r}")


def parse_signin(response: httpx.Response, *, session_token: str) -> Session:
    data = read_json(response)
    if _error_code(data) != 0:
        raise InvalidCredentials(data.get("msg") or "Invalid credentials")
    if response.status_code != 200:
        raise InvalidResponse(f"Signin: unexpected status {response.status_code}")
    return Session(token=_phpsessid(response) or session_token)


def parse_verify_session(response: httpx.Response) -> bool:
    if response.status_code not in (200, 403):
        raise InvalidResponse(
            f"verify_session: unexpected status {response.status_code}"
        )
    data = read_json(response)
    return response.status_code == 200 and _error_code(data) == 0


def parse_signout(response: httpx.Response) -> None:
    if response.status_code != 200:
        raise InvalidResponse(f"signout: unexpected status {response.status_code}")


def parse_request_otp(response: httpx.Response) -> OtpInfo:
    if response.status_code != 200:
        raise InvalidResponse(f"OTP: unexpected status {response.status_code}")

    data = read_json(response)
    email = data.get("femail")
    if not email:
        raise InvalidInput(data.get("msg") or "OTP request failed")
    return OtpInfo(email=email, message=data.get("msg"))


def parse_reset_password(response: httpx.Response) -> None:
    if response.status_code != 200:
        raise InvalidResponse(
            f"reset_password: unexpected status {response.status_code}"
        )
