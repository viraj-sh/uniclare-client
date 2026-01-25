from datetime import timedelta
from typing import Any, Dict, List
from core.utils import EnvManager, standard_response
from core.logging import setup_logging
from core.cache import cached_request, invalidate_cache
from core.exceptions import handle_exception
from .model.model_notifications import Notification


def fetch_notifications(refetch: bool = False) -> Dict[str, Any]:
    logger = setup_logging(name="core.fetch_notifications", level="INFO")
    log_prefix = "[NotificationsAPI] "

    try:
        session_id = EnvManager.get("PHPSESSID", default=None)
        if not session_id:
            logger.warning(f"{log_prefix}Missing PHPSESSID; cannot proceed.")
            return standard_response(False, error="Missing PHPSESSID", status_code=400)
        url = "https://studentportal.universitysolutions.in/src/notificationstatus.php"
        headers = {
            "Host": "studentportal.universitysolutions.in",
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/141.0.0.0 Safari/537.36"
            ),
            "Connection": "keep-alive",
        }
        cookies = {"PHPSESSID": session_id}

        response = cached_request(
            method="POST",
            url=url,
            headers=headers,
            cookies=cookies,
            expire_after=timedelta(minutes=10),
            refetch=refetch,
            log_prefix=log_prefix,
        )

        if not response or response.status_code != 200:
            invalidate_cache(response)
            logger.warning(
                f"{log_prefix}Invalid response (status={getattr(response, 'status_code', 'N/A')})."
            )
            return standard_response(
                False, error="Failed to fetch notifications", status_code=400
            )

        try:
            raw_json = response.json()
        except Exception:
            invalidate_cache(response)
            logger.warning(f"{log_prefix}Malformed JSON response.")
            return standard_response(
                False, error="Malformed response from server", status_code=400
            )

        if not isinstance(raw_json, list):
            invalidate_cache(response)
            logger.warning(
                f"{log_prefix}Unexpected response type (not list). Possibly expired session."
            )
            return standard_response(
                False, error="Invalid or expired session", status_code=400
            )

        notifications: List[Notification] = []
        for item in raw_json:
            notif = Notification.from_json(item)
            if notif:
                notifications.append(notif)
            else:
                logger.warning(
                    f"{log_prefix}Skipped invalid notification entry: {item}"
                )

        data = [n.__dict__ for n in notifications]
        return standard_response(True, data=data, status_code=200)

    except Exception as exc:
        return handle_exception(logger, exc, context="fetch_notifications")
