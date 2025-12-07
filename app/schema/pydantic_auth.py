from pydantic import BaseModel, Field
from typing import Optional, Any, Dict


class AuthRequest(BaseModel):
    phone_number: str = Field(
        ...,
        title="Phone number",
        min_length=10,
        max_length=13,
        example="987654XXXX",
    )
    password: str = Field(
        ...,
        title="Password",
        example="user-password-here",
    )


class AuthData(BaseModel):
    message: Optional[str] = Field(None, alias="msg")
    phpsessid: Optional[str] = Field(None, alias="session_id")
    error_code: Optional[int] = None


class AuthResponse(BaseModel):
    success: bool
    data: Optional[AuthData] = None
    error: Optional[str] = None
    status_code: int


class StandardResponse(BaseModel):
    success: bool = Field(..., title="Success flag")
    error: Optional[str] = Field(None, title="Error message (if any)")
    data: Optional[Dict[str, Any]] = Field(None, title="Payload data")
    status_code: int = Field(..., title="HTTP status code to be returned")


class LogoutResponse(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[Dict[str, Any]] = Field(None)
    status_code: int = Field(...)


class PasswordResetOTPRequest(BaseModel):
    phone_number: str = Field(...)


class StandardResponseData(BaseModel):
    mobile: Optional[str] = Field(None)
    status: Optional[str] = Field(None)


class PasswordResetOTPResponse(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[Dict[str, Any]] = Field(None)
    status_code: int = Field(...)


class PasswordResetRequest(BaseModel):
    mobile: str = Field(..., title="Mobile Number", description="User's mobile number")
    otp: str = Field(..., title="OTP")
    new_password: str = Field(..., title="New Password")


class PasswordResetResponseData(BaseModel):
    mobile: str
    status: str


class PasswordResetResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    status_code: int


class PasswordCheckRequest(BaseModel):
    password: str = Field(
        ...,
        example="MyS3cretP@ssw0rd",
        min_length=1,
    )


class StandardResponseModel(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[Dict[str, Any]] = Field(None)
    status_code: int = Field(...)


class PasswordUpdateRequest(BaseModel):
    new_password: str = Field(..., min_length=6, max_length=128)
