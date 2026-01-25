from typing import Any, Dict
from fastapi import APIRouter, Body
from core.utils import standard_response
from core.logging import setup_logging
from core.exceptions import handle_exception
from services.auth import (
    authenticate_student,
    validate_session,
    logout_user,
    send_password_reset_otp,
    reset_password,
    check_current_password,
    update_password,
)
from schema.pydantic_auth import (
    AuthRequest,
    AuthResponse,
    StandardResponse,
    LogoutResponse,
    PasswordResetOTPRequest,
    PasswordResetOTPResponse,
    PasswordResetRequest,
    PasswordResetResponse,
    PasswordCheckRequest,
    StandardResponseModel,
    PasswordUpdateRequest,
)
from fastapi.responses import JSONResponse

logger = setup_logging(name="api.auth")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=AuthResponse,
    operation_id="auth_login_post",
    summary="Authenticate student (phone + password)",
)
async def login_student(
    body: AuthRequest = Body(..., description="Phone number and password"),
):
    try:
        logger.info(
            "auth/login called",
            extra={"phone_number": body.phone_number},
        )

        registration_number = body.phone_number
        password = body.password

        result = authenticate_student(
            registration_number=registration_number,
            password=password,
        )

        status_code = result.get("status_code", 200)

        return JSONResponse(content=result, status_code=status_code)

    except Exception as exc:
        error_response = handle_exception(logger, exc, context="auth_login")
        error_status = error_response.get("status_code", 500)
        return JSONResponse(content=error_response, status_code=error_status)


@router.get(
    "/validate-session",
    operation_id="auth_validate_session_get",
    summary="Validate current PHP session ID",
    response_model=StandardResponse,
)
def validate_session_endpoint() -> JSONResponse:
    try:
        logger.info("validate-session called (internal PHPSESSID fetch)")

        result = validate_session()

        if not isinstance(result, dict):
            logger.error("validate_session returned unexpected type: %s", type(result))
            fallback = standard_response(
                success=False,
                error="Session validation returned unexpected result.",
                status_code=500,
            )
            return JSONResponse(
                content=fallback, status_code=fallback.get("status_code", 500)
            )

        if "status_code" not in result or "success" not in result:
            logger.warning(
                "validate_session returned dict missing expected keys; normalizing"
            )
            normalized = standard_response(
                success=result.get("success", False),
                error=(
                    result.get("error")
                    if isinstance(result.get("error"), str)
                    else None
                ),
                data=result.get("data"),
                status_code=result.get("status_code", 500),
            )
            return JSONResponse(
                content=normalized, status_code=normalized.get("status_code", 500)
            )

        return JSONResponse(content=result, status_code=result.get("status_code", 200))

    except Exception as exc:
        logger.exception("Unhandled exception in auth.validate_session endpoint")

        exc_result = handle_exception(logger, exc, context="auth_validate_session")
        if isinstance(exc_result, dict) and "status_code" in exc_result:
            return JSONResponse(
                content=exc_result, status_code=exc_result.get("status_code", 500)
            )

        fallback = standard_response(
            success=False,
            error="Unexpected error while validating session.",
            status_code=500,
        )
        return JSONResponse(
            content=fallback, status_code=fallback.get("status_code", 500)
        )


@router.post(
    "/logout",
    operation_id="auth_logout_post",
    summary="Logout current session",
    response_model=LogoutResponse,
)
def logout_user_endpoint() -> JSONResponse:
    logger = setup_logging(name="api.auth_logout")

    try:
        result: Dict[str, Any] = logout_user()
        print(result)
        if not isinstance(result, dict):
            logger.warning("Unexpected response format from logout_user()")
            result = standard_response(
                success=False,
                error="Unexpected response format from internal function",
                status_code=500,
            )

        return JSONResponse(
            content=result,
            status_code=result.get("status_code", 200),
        )

    except Exception as exc:
        return handle_exception(logger, exc, context="auth_logout_endpoint")


@router.post(
    "/password-reset/send-otp",
    response_model=PasswordResetOTPResponse,
    operation_id="auth_send_password_reset_otp_post",
    summary="Send password reset OTP to a user's mobile number",
)
def send_password_reset_otp_endpoint(
    request: PasswordResetOTPRequest = Body(
        ..., description="Request body containing the phone number"
    ),
) -> JSONResponse:
    logger = setup_logging(name="routes.auth_router.send_password_reset_otp_endpoint")
    try:
        result = send_password_reset_otp(mobile=request.phone_number)
        return JSONResponse(content=result, status_code=result.get("status_code", 200))
    except Exception as exc:
        return handle_exception(logger, exc, context="send_password_reset_otp_endpoint")


@router.post(
    "/password-reset/confirm",
    response_model=PasswordResetResponse,
    operation_id="password_reset_confirm_post",
    summary="Confirm password reset using OTP",
)
def password_reset_confirm(request: PasswordResetRequest = Body(...)):
    try:
        result = reset_password(
            mobile=request.mobile, otp=request.otp, new_password=request.new_password
        )

        return JSONResponse(content=result, status_code=result.get("status_code", 200))

    except Exception as exc:
        return handle_exception(logger, exc, context="password_reset_confirm")


@router.post(
    "/password-check",
    response_model=StandardResponseModel,
    operation_id="password_check_post",
)
async def password_check(
    payload: PasswordCheckRequest = Body(...),
) -> JSONResponse:
    logger.info("Received password-check request.")
    try:
        result: Dict[str, Any] = check_current_password(
            password=payload.password,
        )

        if not isinstance(result, dict):
            logger.warning(
                "check_current_password returned non-dict response. Wrapping into standard_response."
            )
            result = standard_response(
                success=False,
                error="Internal error: invalid response from password check.",
                status_code=500,
            )

        status_code = int(result.get("status_code", 500))
        return JSONResponse(content=result, status_code=status_code)

    except Exception as exc:
        logger.exception("Unhandled exception in password_check endpoint.")
        err_result = handle_exception(logger, exc, context="password_check_endpoint")

        if isinstance(err_result, dict):
            return JSONResponse(
                content=err_result, status_code=int(err_result.get("status_code", 500))
            )

        fallback = standard_response(
            success=False,
            error="Internal server error.",
            status_code=500,
        )
        return JSONResponse(content=fallback, status_code=500)


@router.post(
    "/password-update",
    operation_id="password_update_endpoint",
    response_model=StandardResponseModel,
)
async def password_update(payload: PasswordUpdateRequest = Body(...)) -> JSONResponse:
    try:
        new_password: str = payload.new_password

        logger.info("Received request to update password via FastAPI endpoint")

        result: Dict[str, Any] = update_password(new_password=new_password)

        if not isinstance(result, dict):
            logger.error(
                "core.update_password returned a non-dict response; wrapping with standard_response."
            )
            result = standard_response(
                success=False,
                error="Internal error: Invalid response format.",
                status_code=500,
            )

        status_code: int = int(result.get("status_code", 200) or 200)

        logger.info(f"Password update response prepared with status {status_code}")

        return JSONResponse(content=result, status_code=status_code)

    except Exception as exc:
        logger.exception("Unhandled exception in password_update endpoint")
        err_resp = handle_exception(logger, exc, context="password_update")

        if isinstance(err_resp, dict):
            return JSONResponse(
                content=err_resp, status_code=int(err_resp.get("status_code", 500))
            )

        fallback = standard_response(
            success=False, error="Unexpected server error.", status_code=500
        )
        return JSONResponse(content=fallback, status_code=500)
