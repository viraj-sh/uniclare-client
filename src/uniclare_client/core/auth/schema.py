from pydantic import BaseModel, ConfigDict


class Session(BaseModel):
    model_config = ConfigDict(frozen=True)
    token: str


class Captcha(BaseModel):
    model_config = ConfigDict(frozen=True)
    value: int
    session_token: str


class OtpInfo(BaseModel):
    model_config = ConfigDict(frozen=True)
    email: str
    message: str | None = None
