import httpx

from uniclare_client.core.clients.http import read_json
from uniclare_client.core.errors import InvalidResponse
from uniclare_client.core.results.schema import (
    Result,
    ResultInfo,
    ResultSummary,
    StudentDetail,
    SubjectResult,
)


def _error_code(data: dict) -> int:
    raw = data.get("error_code", 0)
    if raw is None:
        return 0
    try:
        return int(raw)
    except (TypeError, ValueError):
        raise InvalidResponse(f"non-integer error_code: {raw!r}")


def _guard_response(response: httpx.Response, *, operation: str) -> dict:
    if response.status_code != 200:
        try:
            data = response.json()
            msg = data.get("msg") or f"HTTP {response.status_code}"
        except ValueError:
            msg = f"HTTP {response.status_code}"
        raise InvalidResponse(f"{operation}: {msg}")

    data = read_json(response)
    if _error_code(data) != 0:
        raise InvalidResponse(f"{operation}: {data.get('msg') or 'vendor error'}")
    return data


def parse_results_list(response: httpx.Response) -> list[ResultSummary]:
    data = _guard_response(response, operation="results_list")
    raw_items = data.get("data")
    if not isinstance(raw_items, list):
        raise InvalidResponse("results_list: 'data' is not a list")

    summaries = [
        ResultSummary(
            year=item["year"],
            exam_name=item["examname"],
            exam_date=item.get("examdate"),
            result_date=item.get("resultdate"),
            rv_result_date=item.get("rvresultdate"),
            reg_no=item["regno"],
            mc_no=item.get("mcnumber"),
            status=item.get("class"),
        )
        for item in raw_items
    ]
    # vendor returns oldest-first; newest-first is more useful
    return summaries[::-1]


def parse_results_details(response: httpx.Response) -> Result:
    data = _guard_response(response, operation="result_details")

    stud = data.get("studDet")
    if not isinstance(stud, dict):
        raise InvalidResponse("result_details: missing 'studDet'")
    body = data.get("body")
    if not isinstance(body, list) or not body:
        raise InvalidResponse("result_details: missing or empty 'body'")

    head = body[0]
    subjects = [
        SubjectResult(
            id=sub.get("sl_no"),
            sub=sub.get("subject"),
            exam_type=sub.get("mthprue"),
            ese_marks=sub.get("uni_exam"),
            viva_marks=sub.get("viva_exam"),
            ia_marks=sub.get("ia_exam"),
            total_marks=sub.get("thtot"),
            credits=sub.get("FCREDITS"),
            grade_points=sub.get("FGP"),
            credit_points=sub.get("FCP"),
            remarks=sub.get("remarks1"),
            grade=sub.get("remarks"),
        )
        for sub in body
    ]

    return Result(
        student_details=StudentDetail(
            sem=stud.get("FEXAMNAME"),
            full_sem=stud.get("FDESCPN"),
            exam_date=stud.get("FRESEXAMDATE"),
            exam_no=stud["FEXAMNO"],  # required
        ),
        result=ResultInfo(
            result=head.get("result"),
            cgpa=head.get("FCGPA"),
            sgpa=head.get("FSGPA"),
            percentage=head.get("FPERCENT"),
        ),
        subjects=subjects,
    )
