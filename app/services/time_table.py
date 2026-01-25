from datetime import timedelta
from typing import Dict, Any
from core.utils import EnvManager, standard_response
from core.logging import setup_logging
from core.cache import cached_request, invalidate_cache
from core.exceptions import handle_exception
import json
from .model.model_time_table import PracticalTimetable


def fetch_practical_timetable(refetch: bool = False) -> Dict[str, Any]:
    logger = setup_logging(name="core.fetch_practical_timetable", level="INFO")

    try:
        phpsessid = EnvManager.get("PHPSESSID", default=None)
        logger.info("Fetched PHPSESSID from EnvManager")

        if not phpsessid:
            return standard_response(False, error="Missing PHPSESSID", status_code=400)

        url = "https://studentportal.universitysolutions.in/src/practicaltimetable.php"
        headers = {
            "Host": "studentportal.universitysolutions.in",
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
            ),
            "Connection": "keep-alive",
        }
        cookies = {"PHPSESSID": phpsessid}
        data = {"screen": "examtimetable"}

        response = cached_request(
            method="POST",
            url=url,
            headers=headers,
            cookies=cookies,
            data=data,
            log_prefix="[PracticalTimetable] ",
            expire_after=timedelta(hours=1),
            refetch=refetch,
        )

        if not response or not hasattr(response, "text"):
            return standard_response(
                False, error="Empty or invalid response", status_code=400
            )

        try:
            raw = (
                response.json()
                if hasattr(response, "json")
                else json.loads(response.text)
            )
        except Exception:
            logger.warning("Invalid JSON response; invalidating cache.")
            invalidate_cache(response)
            return standard_response(
                False, error="Malformed JSON from server", status_code=400
            )

        parsed = PracticalTimetable.from_json(raw)
        if not parsed:
            invalidate_cache(response)
            return standard_response(
                False,
                error="Invalid or expired session / malformed data",
                status_code=400,
            )

        result_dict = {
            "stud_name": parsed.stud_name,
            "degree_name": parsed.degree_name,
            "sem": parsed.sem,
            "reg_no": parsed.reg_no,
            "center_name": parsed.center_name,
            "subjects": [s.__dict__ for s in parsed.subjects],
        }

        return standard_response(True, data=result_dict, status_code=200)

    except Exception as exc:
        return handle_exception(logger, exc, context="fetch_practical_timetable")
