import logging
from typing import Any

from pydantic import BaseModel

from uniclare_client.core.api import App
from uniclare_client.core.errors import AppError

log = logging.getLogger(__name__)


def _jsonable(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


class JsApi:
    """Every public method here is callable from JavaScript as `api.method(args)`.
    Internals are underscore-prefixed. Never expose App or the runner directly."""

    def __init__(self, runner: Any, app: App) -> None:
        self._runner = runner
        self._app = app

    # ---- helpers ---------------------------------------------------------

    def _err(self, code: str, message: str) -> dict:
        return {"ok": False, "error": {"code": code, "message": message}}

    def _call(self, coro: Any) -> dict:
        try:
            return {"ok": True, "data": _jsonable(self._runner.run(coro))}
        except AppError as exc:
            return self._err(exc.code, exc.message)
        except Exception:
            log.exception("Unhandled error in js_api call")
            return self._err("internal_error", "Unexpected error")

    def _require_token(self, args: dict) -> str | None:
        token = args.get("token", "")
        return token or None

    # ---- auth ------------------------------------------------------------

    def get_captcha(self, args: dict | None = None) -> dict:
        return self._call(self._app.auth.get_captcha())

    def login(self, args: dict) -> dict:
        mobile = args["mobile"]
        password = args["password"]
        captcha_code = int(args["captcha_code"])
        captcha_token = args["captcha_token"]

        async def _do():
            session = await self._app.auth.login(
                reg_no=mobile,
                password=password,
                captcha_code=captcha_code,
                session_token=captcha_token,
            )
            return {"session_token": session.token}

        return self._call(_do())

    def logout(self, args: dict) -> dict:
        token = self._require_token(args)
        if token is None:
            return {"ok": True, "data": None}

        async def _do():
            try:
                await self._app.auth.logout(token)
            except AppError:
                pass
            return None

        return self._call(_do())

    def status(self, args: dict) -> dict:
        token = self._require_token(args)
        if token is None:
            return {"ok": True, "data": False}
        return self._call(self._app.auth.verify_session(token))

    def request_otp(self, args: dict) -> dict:
        mobile_no = args["mobile_no"]

        async def _do():
            return await self._app.auth.request_otp(mobile_no=mobile_no)

        return self._call(_do())

    def reset_password(self, args: dict) -> dict:
        mobile_no = args["mobile_no"]
        otp_code = args["otp_code"]
        new_password = args["new_password"]
        session_token = args["session_token"]

        async def _do():
            await self._app.auth.reset_password(
                mobile_no=mobile_no,
                otp_code=otp_code,
                new_password=new_password,
                session_token=session_token,
            )
            return None

        return self._call(_do())

    # ---- data ------------------------------------------------------------

    def get_profile(self, args: dict) -> dict:
        token = self._require_token(args)
        if token is None:
            return self._err("authentication_error", "Not logged in")
        return self._call(self._app.profile.get(token))

    def get_results(self, args: dict) -> dict:
        token = self._require_token(args)
        if token is None:
            return self._err("authentication_error", "Not logged in")
        return self._call(self._app.results.list(token))

    def get_result(self, args: dict) -> dict:
        token = self._require_token(args)
        if token is None:
            return self._err("authentication_error", "Not logged in")
        return self._call(
            self._app.results.details(
                exam_no=args["exam_no"],
                reg_no=args["reg_no"],
                session_token=token,
            )
        )

    def get_notifications(self, args: dict) -> dict:
        token = self._require_token(args)
        if token is None:
            return self._err("authentication_error", "Not logged in")
        limit = int(args.get("limit", 20))

        async def _do():
            items = await self._app.notifications.list(token)
            return items[: max(0, limit)]

        return self._call(_do())

    # ---- system ----------------------------------------------------------

    def health(self, args: dict | None = None) -> dict:
        return self._call(self._app.health())
