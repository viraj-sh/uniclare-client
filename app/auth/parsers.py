import httpx

from app.auth.schemas import (
    CaptchaResult,
    OTPResult,
    ResetPassResult,
    SigninResult,
    SignoutResult,
    VerifySessionResult,
)


def parse_signin(response: httpx.Response) -> SigninResult:
    data = response.json()
    if response.status_code != 200 or data.get("error_code") == -1:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Signin failed with {response.status_code}"
        )
    ec = data.get("error_code")
    return SigninResult(error_code=ec, message=data.get("msg"))


def parse_captcha(response: httpx.Response) -> CaptchaResult:
    captcha = response.json().get("captcha")

    if response.status_code != 200 or not captcha:
        raise ValueError(f"Captcha failed with {response.status_code}")
    return CaptchaResult(
        captcha=captcha, session_token=response.cookies.get("PHPSESSID")
    )


def parse_verify_session(response: httpx.Response) -> VerifySessionResult:
    data = response.json()
    if (response.status_code != 200 and response.status_code != 403) or data.get(
        "error_code"
    ) == -1:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Session Verification failed with {response.status_code}"
        )
    ec = data.get("error_code")
    status = data.get("status")
    msg = data.get("message")

    return VerifySessionResult(error_code=ec, status=status, message=msg)


def parse_signout(response: httpx.Response) -> SignoutResult:
    data = response.text
    if response.status_code != 200:
        raise ValueError(f"Signout failed with {response.status_code}")
    return SignoutResult(message=data)


def parse_otp(response: httpx.Response) -> OTPResult:
    data = response.json()

    if response.status_code != 200:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Signin failed with {response.status_code}"
        )
    email = data.get("femail")
    status = data.get("status")
    msg = data.get("msg")
    return OTPResult(email=email, message=msg, status=status)


def parse_reset_password(response: httpx.Response) -> ResetPassResult:
    data = response.json()

    if response.status_code != 200:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Signin failed with {response.status_code}"
        )
    status = data.get("status")
    return ResetPassResult(status=status)
