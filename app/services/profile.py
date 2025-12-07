import requests
from typing import Optional, Dict, Any
from datetime import timedelta
from core.utils import EnvManager, standard_response
from core.logging import setup_logging
from core.cache import cached_request, invalidate_cache
from core.exceptions import handle_exception
from .model.model_profile import StudentProfile, EditableProfile


def fetch_profile(refetch: bool = False) -> Dict[str, any]:
    logger = setup_logging(name="core.fetch_profile", level="INFO")
    log_prefix = "[StudentProfile] "

    try:
        phpsessid = EnvManager.get("PHPSESSID", default=None)
        if not phpsessid:
            logger.warning(f"{log_prefix}No PHPSESSID found in environment")
            return standard_response(
                False, error_msg="Missing session ID", status_code=400
            )
        logger.info(f"{log_prefix}Fetched PHPSESSID from EnvManager")

        url = "https://studentportal.universitysolutions.in/src/profile.php"
        headers = {"Cookie": f"PHPSESSID={phpsessid}"}

        response = cached_request(
            method="POST",
            url=url,
            headers=headers,
            timeout=10,
            log_prefix=log_prefix,
            expire_after=timedelta(hours=1),
            refetch=refetch,
        )

        try:
            data = response.json()
        except ValueError:
            invalidate_cache(response)
            logger.warning(f"{log_prefix}Invalid JSON received, cache invalidated")
            return standard_response(
                False, error_msg="Invalid response from server", status_code=400
            )

        profile = StudentProfile.from_json(data)
        if not profile:
            invalidate_cache(response)
            logger.warning(
                f"{log_prefix}Profile data invalid or incomplete, cache invalidated"
            )
            return standard_response(
                False, error_msg="Profile not found or invalid", status_code=404
            )

        logger.info(
            f"{log_prefix}Profile fetched successfully for reg_no: {profile.reg_no}"
        )
        return standard_response(True, data=profile.__dict__, status_code=200)

    except Exception as exc:
        return handle_exception(logger, exc, context="fetch_profile")


def fetch_editable_profile(refetch: bool = False) -> Dict[str, Any]:
    logger = setup_logging(name="core.fetch_editable_profile", level="INFO")

    try:
        phpsessid = EnvManager.get("PHPSESSID", default=None)
        if not phpsessid:
            return standard_response(
                False, error_msg="Missing PHPSESSID", status_code=400
            )
        logger.info("Fetched PHPSESSID from EnvManager")

        url = "https://studentportal.universitysolutions.in/app.php?a=getStudDet&univcode=051"
        headers = {"Cookie": f"PHPSESSID={phpsessid}"}

        response = cached_request(
            method="POST",
            url=url,
            headers=headers,
            timeout=10,
            log_prefix="[FetchProfile] ",
            expire_after=timedelta(minutes=10),
            refetch=refetch,
        )

        if response.status_code != 200:
            invalidate_cache(response)
            return standard_response(
                False,
                error_msg=f"Invalid response status {response.status_code}",
                status_code=response.status_code,
            )

        try:
            data = response.json() if hasattr(response, "json") else dict(response)
        except Exception:
            invalidate_cache(response)
            return standard_response(
                False, error_msg="Failed to parse response JSON", status_code=400
            )

        profile = EditableProfile.from_json(data)
        if profile is None:
            invalidate_cache(response)
            return standard_response(
                False, error_msg="Profile data missing or malformed", status_code=400
            )

        return standard_response(True, data=profile.__dict__, status_code=200)

    except Exception as exc:
        return handle_exception(logger, exc, context="fetch_editable_profile")


def update_editable_profile(
    ffatname: Optional[str] = None,
    fmotname: Optional[str] = None,
    fabcno: Optional[str] = None,
) -> Dict[str, Any]:
    logger = setup_logging(name="core.update_editable_profile", level="INFO")

    try:
        phpsessid = EnvManager.get("PHPSESSID", default=None)
        if not phpsessid:
            logger.warning("PHPSESSID not provided or found in environment.")
            return standard_response(
                False, error_msg="Session ID missing", status_code=400
            )

        current_profile_resp = fetch_editable_profile(phpsessid)
        current_profile = current_profile_resp.get("data", {})
        if not current_profile:
            logger.warning("Failed to fetch current editable profile.")
            return standard_response(
                False, error_msg="Could not fetch current profile", status_code=404
            )

        payload = {
            "reg_no": current_profile.get("reg_no"),
            "fstudname": current_profile.get("full_name"),
            "ffatname": ffatname or current_profile.get("fath_name"),
            "fmotname": fmotname or current_profile.get("mot_name"),
            "fabcno": fabcno or current_profile.get("abc_id"),
        }

        url = "https://studentportal.universitysolutions.in/app.php?a=saveStudDet&univcode=051"
        headers = {
            "Cookie": f"PHPSESSID={phpsessid}",
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "Host": "studentportal.universitysolutions.in",
            "Connection": "keep-alive",
        }

        response = requests.post(url, headers=headers, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            result = {
                "ffatname": payload["ffatname"],
                "fmotname": payload["fmotname"],
                "fabcno": payload["fabcno"],
            }
            logger.info("Profile updated successfully.")
            return standard_response(True, data=result, status_code=200)
        else:
            logger.warning(f"Profile update failed: {data}")
            return standard_response(
                False, error_msg="Profile update failed", status_code=400
            )

    except Exception as exc:
        return handle_exception(logger, exc, context="update_editable_profile")
