from app.auth.schemas import (
    CaptchaResult,
    SigninResult,
    SignoutResult,
    VerifySessionResult,
)
from app.auth.service import get_captcha, logout
from app.auth.service import login as auth_login
from app.auth.service import verify_session as verify_session


class App:
    async def login(
        self, mobile_no: str, password: str, captcha: int, session_token: str
    ) -> SigninResult:
        return await auth_login(mobile_no, password, captcha, session_token)

    async def captcha(self) -> CaptchaResult:
        return await get_captcha()

    async def verify_session_token(self, session_token: str) -> VerifySessionResult:
        return await verify_session(session_token)

    async def logout(self, session_token: str) -> SignoutResult:
        return await logout(session_token)


app = App()
