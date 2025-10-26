from datetime import timedelta
from typing import Optional, Dict, Any, List

from core.utils import EnvManager, standard_response
from core.logging import setup_logging
from core.cache import cached_request, invalidate_cache
from core.exceptions import handle_exception
from .model.model_result import StudentResult, ExamResult, SubjectsResult

logger = setup_logging(name="core.result", level="INFO")


def fetch_student_results(refetch: bool = False) -> Dict[str, Any]:
    log_prefix = "[StudentResults] "

    try:
        session_id = EnvManager.get("PHPSESSID", default=None)
        if not session_id:
            logger.warning(f"{log_prefix}Missing PHPSESSID. Cannot fetch results.")
            return standard_response(
                success=False,
                error_msg="Missing session ID. Please log in again.",
                status_code=401,
            )

        url = "https://studentportal.universitysolutions.in/src/results_new.php"
        headers = {
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "Host": "studentportal.universitysolutions.in",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        }
        params = {"a": "getResAll"}
        cookies = {"PHPSESSID": session_id}

        response = cached_request(
            method="GET",
            url=url,
            headers=headers,
            params=params,
            cookies=cookies,
            log_prefix=log_prefix,
            expire_after=timedelta(hours=1),
            refetch=refetch,
        )

        if not response or response.status_code != 200:
            logger.warning(f"{log_prefix}Invalid or empty response.")
            if response:
                invalidate_cache(response)
            return standard_response(
                success=False,
                error_msg="Failed to fetch results from the student portal.",
                status_code=400,
            )

        try:
            data = response.json()
        except ValueError as e:
            logger.error(f"{log_prefix}Invalid JSON response: {e}")
            invalidate_cache(response)
            return standard_response(
                success=False,
                error_msg="Invalid response format from the server.",
                status_code=502,
            )

        if (
            not isinstance(data, dict)
            or data.get("error_code") != 0
            or "data" not in data
        ):
            logger.warning(f"{log_prefix}Unexpected payload or error from API.")
            invalidate_cache(response)
            return standard_response(
                success=False,
                error_msg="Invalid or expired session. Please log in again.",
                status_code=403,
            )

        raw_results = data.get("data", [])
        parsed_results: List[Dict[str, Any]] = []

        for item in raw_results:
            result_obj = StudentResult.from_json(item)
            if result_obj:
                parsed_results.append(result_obj.__dict__)

        if not parsed_results:
            logger.warning(
                f"{log_prefix}Response did not match expected model structure."
            )
            invalidate_cache(response)
            return standard_response(
                success=False,
                error_msg="Unexpected data structure received. Cache invalidated.",
                status_code=422,
            )

        logger.info(
            f"{log_prefix}Fetched {len(parsed_results)} valid results successfully."
        )
        return standard_response(
            success=True,
            data=parsed_results,
            status_code=200,
        )

    except Exception as exc:
        return handle_exception(logger, exc, context="fetch_student_results")


def fetch_exam_result(
    exam_code: Optional[str] = None, refetch: bool = False
) -> Dict[str, Any]:
    log_prefix = "[ExamResult] "

    try:
        if not exam_code:
            return standard_response(
                success=False,
                error_msg="Exam code is required.",
                status_code=400,
            )

        phpsessid = EnvManager.get("PHPSESSID", default=None)

        if not phpsessid:
            return standard_response(
                success=False,
                error_msg="Missing or invalid PHPSESSID.",
                status_code=401,
            )

        url = (
            f"https://studentportal.universitysolutions.in/src/results_new.php"
            f"?a=getResults&examno={exam_code}"
        )
        headers = {
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "Host": "studentportal.universitysolutions.in",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        }
        cookies = {"PHPSESSID": phpsessid}

        response = cached_request(
            method="GET",
            url=url,
            headers=headers,
            cookies=cookies,
            timeout=30,
            refetch=refetch,
            expire_after=timedelta(hours=12),
            log_prefix=log_prefix,
        )

        if not response or response.status_code != 200:
            logger.warning(f"{log_prefix}Invalid or empty response.")
            invalidate_cache(response)
            return standard_response(
                success=False,
                error_msg="Failed to fetch exam result.",
                status_code=response.status_code if response else 500,
            )

        try:
            data = response.json()
        except Exception as json_err:
            logger.warning(f"{log_prefix}Invalid JSON response: {json_err}")
            invalidate_cache(response)
            return standard_response(
                success=False,
                error_msg="Invalid JSON response.",
                status_code=502,
            )

        exam_result = ExamResult.from_json(data)
        if exam_result is None:
            logger.warning(
                f"{log_prefix}Response validation failed. Invalidating cache."
            )
            invalidate_cache(response)
            return standard_response(
                success=False,
                error_msg="Unexpected or malformed data format.",
                status_code=422,
            )

        result_dict = exam_result.to_dict()
        logger.info(f"{log_prefix}Exam result fetched successfully.")
        return standard_response(
            success=True,
            data=result_dict,
            status_code=200,
        )

    except Exception as exc:
        return handle_exception(logger, exc, context="fetch_exam_result")


def fetch_detailed_exam_result(
    exam_code: Optional[str] = None, refetch: bool = False
) -> Dict[str, Any]:
    logger = setup_logging(name="core.fetch_detailed_exam_result", level="INFO")

    try:
        phpsessid = EnvManager.get("PHPSESSID", default=None)
        if phpsessid is None:
            return standard_response(
                False, error_msg="PHPSESSID not found", status_code=400
            )

        if not exam_code:
            return standard_response(
                False, error_msg="exam_code is required", status_code=400
            )

        url = f"https://studentportal.universitysolutions.in/src/results_new.php?a=getResDet&examno={exam_code}"
        headers = {
            "Referer": "https://studentportal.universitysolutions.in/MainPage.html",
            "Host": "studentportal.universitysolutions.in",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        }
        cookies = {"PHPSESSID": phpsessid}

        response = cached_request(
            "GET",
            url,
            headers=headers,
            cookies=cookies,
            timeout=30,
            log_prefix="[ExamResult] ",
            expire_after=timedelta(hours=1),
            refetch=refetch,
        )

        data = response.json().get("data", {})
        if not data:
            invalidate_cache(response)
            return standard_response(
                False, error_msg="No data found in response", status_code=404
            )

        subjects: List[Dict[str, Any]] = []
        for sub_name, exams_dict in data.items():
            subject_result = SubjectsResult.from_json(sub_name, exams_dict)
            if subject_result:
                subjects.append(
                    {
                        "sub_name": subject_result.sub_name,
                        **{
                            exam_code: {
                                "exam_type": detail.exam_type,
                                "remark": detail.remark,
                                "type": detail.type,
                            }
                            for exam_code, detail in subject_result.exams.items()
                        },
                    }
                )

        return standard_response(True, data={"subjects": subjects}, status_code=200)

    except Exception as exc:
        return handle_exception(logger, exc, context="fetch_detailed_exam_result")
