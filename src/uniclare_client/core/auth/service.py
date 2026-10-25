from uniclare_client.core.auth import endpoints, parsers
from uniclare_client.core.auth.schema import Captcha, OtpInfo, Session
from uniclare_client.core.clients.http import HttpClient


class AuthService:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def get_captcha(self) -> Captcha:
        return parsers.parse_captcha(await endpoints.captcha(self._http))

    async def login(
        self,
        *,
        reg_no: str,
        password: str,
        captcha_code: int,
        session_token: str,
    ) -> Session:
        response = await endpoints.signin(
            self._http,
            reg_no=reg_no,
            password=password,
            captcha_code=captcha_code,
            session_token=session_token,
        )
        return parsers.parse_signin(response, session_token=session_token)

    async def verify_session(self, session_token: str) -> bool:
        print(session_token)
        return parsers.parse_verify_session(
            await endpoints.verify_session(self._http, session_token)
        )

    async def logout(self, session_token: str) -> None:
        parsers.parse_signout(await endpoints.signout(self._http, session_token))

    async def request_otp(self, *, mobile_no: str) -> OtpInfo:
        return parsers.parse_request_otp(
            await endpoints.request_otp(self._http, mobile_no=mobile_no)
        )

    async def reset_password(
        self,
        *,
        mobile_no: str,
        otp_code: str,
        new_password: str,
        session_token: str,
    ) -> None:
        parsers.parse_reset_password(
            await endpoints.reset_password(
                self._http,
                mobile_no=mobile_no,
                otp_code=otp_code,
                new_password=new_password,
                session_token=session_token,
            )
        )
