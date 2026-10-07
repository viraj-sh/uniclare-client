import json
import re

import httpx

from app.auth.schemas import CaptchaResult, SigninResult


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
        raise ValueError(f"Captha failed with {response.status_code}")
    return CaptchaResult(captcha=captcha, session_id=response.cookies.get("PHPSESSID"))


def _extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines:
        last = lines[-1]
        if last.startswith("{") and last.endswith("}"):
            try:
                return json.loads(last)
            except json.JSONDecodeError:
                pass

    matches = list(re.finditer(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", text, re.DOTALL))
    if matches:
        candidate = matches[-1].group()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError("No valid JSON found in the response.")
