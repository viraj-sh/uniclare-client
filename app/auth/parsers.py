import httpx

from app.auth.schemas import CaptchaResult, SigninResult, VerifySessionResult


def parse_signin(response: httpx.Response) -> SigninResult:
    data = response.json()
    if response.status_code != 200 or data.get("error_code") == -1:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Signin failed with {response.status_code}"
        )
    ec = data.get("error_code")
    return SigninResult(error_code=ec, msg=data.get("msg"))


def parse_captcha(response: httpx.Response) -> CaptchaResult:
    captcha = response.json().get("captcha")

    if response.status_code != 200 or not captcha:
        raise ValueError(f"Captcha failed with {response.status_code}")
    return CaptchaResult(
        captcha=captcha, session_token=response.cookies.get("PHPSESSID")
    )


def parse_verify_session(response: httpx.Response) -> VerifySessionResult:
    data = response.json()
    if response.status_code != 200 or data.get("error_code") == -1:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Session Verification failed with {response.status_code}"
        )
    ec = data.get("error_code")
    return VerifySessionResult(error_code=ec, status=data.get("status"))
