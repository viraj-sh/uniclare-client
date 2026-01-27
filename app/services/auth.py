from typing import Optional, Any, Dict
import requests
from core.utils import EnvManager, standard_response
from core.logging import setup_logging
from core.cache import clear_cache
import json
from core.exceptions import handle_exception


def authenticate_student(registration_number: str, password: str) -> Dict[str, Any]:
    logger = setup_logging(name="student-auth", level="INFO")
    url = "https://studentportal.universitysolutions.in/signin.php"
    session = requests.Session()

    try:
        logger.info("Authenticating student", extra={"reg_no": registration_number})

        response = session.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"regno": registration_number, "passwd": password},
            timeout=50,
        )

        if response.status_code != 200:
            logger.warning(f"Unexpected HTTP status: {response.status_code}")
            return standard_response(
                success=False,
                error=f"Unexpected HTTP status: {response.status_code}",
                status_code=response.status_code,
            )

        try:
            payload = response.json()
        except ValueError:
            logger.error("Invalid JSON response from server")
            return standard_response(
                False, error="Invalid JSON response from server", status_code=502
            )

        error_code = int(payload.get("error_code", -1))
        msg = payload.get("msg", "Unknown response message")
        session_id: Optional[str] = session.cookies.get("PHPSESSID")

        if error_code == 0 and session_id:
            try:
                EnvManager.set("PHPSESSID", session_id)
                logger.info("PHPSESSID successfully saved to .env")
            except RuntimeError as e:
                logger.error(f"Failed to persist PHPSESSID: {str(e)}")

            return standard_response(
                True,
                data={"session_id": session_id, "msg": msg, "error_code": error_code},
                status_code=200,
            )

        logger.warning(f"Authentication failed: {msg}")
        return standard_response(False, error=msg, status_code=401)

    except Exception as e:
        return handle_exception(logger, e)


def validate_session(phpsessid: Optional[str] = None) -> Dict[str, Any]:
    logger = setup_logging(name="core.validate_session", level="INFO")
    url = "https://studentportal.universitysolutions.in/src/profile.php"

    try:
        if not phpsessid:
            phpsessid = EnvManager.get("PHPSESSID", default=None)
            logger.info(
                f"EnvManager retrieval: PHPSESSID {'found' if phpsessid else 'not found'}"
            )

        if not phpsessid:
            logger.warning("Session validation skipped: No PHPSESSID available")
            return standard_response(
                False,
                error="No active session found. Please log in again.",
                status_code=400,
            )

        headers = {
            "Cookie": f"PHPSESSID={phpsessid}",
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "Host": "studentportal.universitysolutions.in",
            "Connection": "keep-alive",
        }

        response = requests.post(url, headers=headers, timeout=50)

        if response.status_code != 200:
            logger.warning(
                f"Session validation failed: Non-200 HTTP response ({response.status_code})"
            )
            return standard_response(
                False,
                error="Failed to validate session (non-200 response).",
                status_code=400,
            )

        try:
            data = response.json() if response.text.startswith("{") else {}
        except json.JSONDecodeError:
            data = {}

        is_valid = data.get("status") == "success"

        if is_valid:
            logger.info("Session validation successful: Session is active")
            return standard_response(
                True,
                data={"session_valid": True, "message": "Session is active"},
                status_code=200,
            )

        logger.warning("Session invalid or expired")
        return standard_response(
            False, error="Session expired or invalid.", status_code=401
        )

    except Exception as exc:
        result = handle_exception(logger, exc)
        if not isinstance(result, dict):
            return standard_response(
                False,
                error="Unexpected error during session validation",
                status_code=500,
            )
        return result


def logout_user() -> Dict[str, Any]:
    logger = setup_logging(name="core.logout_user", level="INFO")
    url = "https://studentportal.universitysolutions.in/src/logout.php"

    phpsessid = EnvManager.get("PHPSESSID", default=None)
    logger.info(
        f"EnvManager retrieval: PHPSESSID {'found' if phpsessid else 'not found'}"
    )

    if not phpsessid:
        logger.warning("Logout skipped: No PHPSESSID available")
        return standard_response(
            False, error="No active session found. Cannot logout.", status_code=400
        )

    headers = {
        "Cookie": f"PHPSESSID={phpsessid}",
        "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
        "Host": "studentportal.universitysolutions.in",
        "Connection": "keep-alive",
    }

    logger.info(f"Logout initiated for PHPSESSID: {phpsessid}")

    try:
        response = requests.post(url, headers=headers, timeout=50)

        if response.status_code != 200:
            logger.warning(
                f"Logout failed: Non-200 status code ({response.status_code})"
            )
            return standard_response(
                False,
                error="Logout request failed with non-200 response",
                status_code=400,
            )

        session_result = validate_session(phpsessid)
        if not isinstance(session_result, dict):
            session_result = {}

        data_dict = session_result.get("data") or {}
        session_valid = data_dict.get("session_valid", False)
        logger.info(
            f"Session validation after logout: {'active' if session_valid else 'terminated'}"
        )

        if not session_valid:
            EnvManager.unset("PHPSESSID")
            logger.info("PHPSESSID removed from environment")

            clear_cache()

            result_data = {"phpsessid": phpsessid, "message": "Logout successful"}
            logger.info(f"Logout successful for PHPSESSID: {phpsessid}")
            return standard_response(True, data=result_data, status_code=200)

        logger.warning("Logout unsuccessful: Session still valid")
        return standard_response(
            False,
            error="Session still active. Logout not confirmed.",
            status_code=400,
        )

    except Exception as exc:
        logger.exception(f"Exception during logout: {exc}")
        return handle_exception(logger, exc)


def send_password_reset_otp(mobile: str) -> Dict[str, Any]:
    logger = setup_logging(name="core.send_password_reset_otp", level="INFO")
    url = "https://studentportal.universitysolutions.in/forgot-password.php"
    payload = {"mobile": mobile}

    logger.info("Attempting to send password reset OTP", extra={"mobile": mobile})

    try:
        response = requests.post(url, data=payload, timeout=50)
        response.raise_for_status()
        data = response.json()
        logger.info("Received response from OTP endpoint", extra={"response": data})

        if data.get("status") == "success":
            logger.info("OTP sent successfully")
            return standard_response(
                success=True,
                data={"mobile": mobile, "status": "OTP sent"},
                status_code=200,
            )

        error = data.get("message", "Failed to send OTP")
        logger.warning("OTP not sent", extra={"error": error})
        return standard_response(success=False, error=error, status_code=400)

    except Exception as exc:
        return handle_exception(logger, exc)


def reset_password(mobile: str, otp: str, new_password: str) -> Dict[str, Any]:
    logger = setup_logging(name="core.reset_password", level="INFO")
    url = "https://studentportal.universitysolutions.in/resetpassword.php"
    payload = {"mobile": mobile, "otp": otp, "password": new_password}

    logger.info("Attempting to reset password", extra={"mobile": mobile})

    try:
        response = requests.post(url, data=payload, timeout=50)
        response.raise_for_status()
        data = response.json()
        logger.info(
            "Received response from reset password endpoint", extra={"response": data}
        )

        if data.get("status") == "success":
            logger.info("Password reset successful", extra={"mobile": mobile})
            return standard_response(
                success=True,
                data={"mobile": mobile, "status": "Password reset successful"},
                status_code=200,
            )

        error = data.get("message", "Failed to reset password")
        logger.warning(
            "Password reset failed", extra={"mobile": mobile, "error": error}
        )
        return standard_response(success=False, error=error, status_code=400)

    except Exception as exc:
        return handle_exception(logger, exc)


def check_current_password(password: str) -> Dict[str, Any]:
    logger = setup_logging(name="core.check_current_password", level="INFO")

    try:
        session_id = EnvManager.get("PHPSESSID", default=None)
        if not session_id:
            logger.warning("Missing PHPSESSID in environment or function argument.")
            return standard_response(
                success=False,
                error="Missing PHPSESSID. User not authenticated.",
                status_code=400,
            )

        url = "https://studentportal.universitysolutions.in/src/chngPassword.php?action=chkUser"
        headers = {
            "Host": "studentportal.universitysolutions.in",
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/141.0.0.0 Safari/537.36"
            ),
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        cookies = {"PHPSESSID": session_id}
        data = {"passwd": password}

        logger.info("Sending password verification request to Uniclare API.")
        response = requests.post(
            url, headers=headers, cookies=cookies, data=data, timeout=50
        )
        response.raise_for_status()

        raw = response.json()
        logger.info(f"Received response: {raw}")

        status = raw.get("status")
        error_code = raw.get("error_code")

        if status == "success" and error_code == 0:
            return standard_response(
                success=True,
                data={"message": "Password is correct."},
                status_code=200,
            )

        elif status == "failure" and error_code == -1:
            return standard_response(
                success=False,
                error="Incorrect password.",
                status_code=400,
            )

        else:
            logger.warning("Unexpected response format received from API.")
            return standard_response(
                success=False,
                error="Unexpected response format.",
                status_code=400,
            )

    except Exception as exc:
        return handle_exception(logger, exc, context="check_current_password")


def update_password(new_password: str = "") -> Dict[str, Any]:  # nosec
    logger = setup_logging(name="core.update_password", level="INFO")
    url = "https://studentportal.universitysolutions.in/src/chngPassword.php?action=updatePassword"

    try:
        phpsessid = EnvManager.get("PHPSESSID", default=None)
        logger.info("Fetched PHPSESSID from EnvManager")

        if not phpsessid:
            logger.warning("Missing PHPSESSID; cannot authenticate user.")
            return standard_response(
                success=False,
                error="Missing PHPSESSID. Please log in again.",
                status_code=401,
            )

        headers = {
            "Host": "studentportal.universitysolutions.in",
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/141.0.0.0 Safari/537.36"
            ),
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        cookies = {"PHPSESSID": phpsessid}
        data = {"passwd": new_password}

        logger.info("Sending password update request to Uniclare API")
        response = requests.post(
            url, headers=headers, cookies=cookies, data=data, timeout=50
        )
        response.raise_for_status()

        raw = response.json()
        logger.info("Received response from API")

        if raw.get("status") == "success" and raw.get("error_code") == 0:
            msg = raw.get("msg", "Password updated successfully.")
            logger.info("Password updated successfully for user session.")
            return standard_response(
                success=True,
                data={"message": msg},
                status_code=200,
            )

        msg = raw.get("msg", "Failed to update password.")
        logger.warning(f"Password update failed: {msg}")
        return standard_response(
            success=False,
            error=msg,
            data={"raw_response": raw},
            status_code=400,
        )

    except Exception as exc:
        return handle_exception(logger, exc, context="update_password")
