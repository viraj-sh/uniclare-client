from app.auth.schemas import (
    CaptchaResult,
    OTPResult,
    ResetPassResult,
    SigninResult,
    SignoutResult,
    VerifySessionResult,
)
from app.auth.service import get_captcha, get_otp, logout, reset_pass
from app.auth.service import login as auth_login
from app.auth.service import verify_session as verify_session
from app.notifications.schemas import NotificationResponse
from app.notifications.service import noti
from app.profile.schemas import ProfileResult
from app.profile.service import profile as get_profile
from app.results.schemas import Result, ResultListResult
from app.results.service import list_result, result_det


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

    async def otp(self, mobile_no: str, session_token: str) -> OTPResult:
        return await get_otp(mobile_no, session_token)

    async def reset_password(
        self,
        mob_no: str,
        otp: str,
        new_password: str,
        session_token: str,
    ) -> ResetPassResult:
        return await reset_pass(mob_no, otp, new_password, session_token)

    async def profile(self, session_token: str) -> ProfileResult:
        return await get_profile(session_token)

    async def results_list(self, session_token: str) -> list[ResultListResult]:
        return await list_result(session_token)

    async def result_details(
        self,
        exam_no: str,
        reg_no: str,
        session_token: str,
    ) -> Result:
        return await result_det(exam_no, reg_no, session_token)

    async def notifications(self, session_token: str) -> list[NotificationResponse]:
        return await noti(session_token)


app = App()
