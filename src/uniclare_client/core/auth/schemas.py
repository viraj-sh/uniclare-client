from typing import Optional

from pydantic import BaseModel, Field


class SigninResult(BaseModel):
    status_code: Optional[int] = Field(None)
    error_code: Optional[str] = Field(None)
    message: Optional[str] = Field(None)


class CaptchaResult(BaseModel):
    status_code: Optional[int] = Field(None)
    captcha: Optional[int] = Field(None)
    session_token: Optional[str] = Field(None)


class VerifySessionResult(BaseModel):
    status_code: Optional[int] = Field(None)
    error_code: Optional[int] = Field(None)
    status: Optional[str] = Field(None)
    message: Optional[str] = Field(None)


class SignoutResult(BaseModel):
    status_code: Optional[int] = Field(None)
    message: Optional[str] = Field(None)


class OTPResult(BaseModel):
    status_code: Optional[int] = Field(None)
    email: Optional[str] = Field(None)
    message: Optional[str] = Field(None)
    status: Optional[str] = Field(None)


class ResetPassResult(BaseModel):
    status_code: Optional[int] = Field(None)
    status: Optional[str] = Field(None)
