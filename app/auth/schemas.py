from typing import Optional

from pydantic import BaseModel, Field


class SigninResult(BaseModel):
    error_code: Optional[str] = Field(None)
    msg: Optional[str] = Field(None)


class CaptchaResult(BaseModel):
    captcha: Optional[int] = Field(None)
    session_token: Optional[str] = Field(None)


class VerifySessionResult(BaseModel):
    error_code: Optional[int] = Field(None)
    status: Optional[str] = Field(None)
