from app.auth.schemas import CaptchaResult, SigninResult
from app.auth.service import get_captcha
from app.auth.service import login as auth_login


class App:
    async def login(
        self, mobile_no: str, password: str, captcha: int, session_id: str
    ) -> SigninResult:
        return await auth_login(mobile_no, password, captcha, session_id)

    async def captcha(self) -> CaptchaResult:
        return await get_captcha()


app = App()
