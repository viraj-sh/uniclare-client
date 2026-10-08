import httpx

from app.results.schemas import (
    Result,
    ResultInfo,
    ResultListResult,
    StudentDetail,
    SubjectResult,
)


def parse_results_list(response: httpx.Response) -> list[ResultListResult]:
    data = response.json()
    if response.status_code != 200:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Fetching User Profile with {response.status_code}"
        )
    return [
        ResultListResult(
            year=result.get("year"),
            exam_date=result.get("examdate"),
            exam_name=result.get("examname"),
            result_date=result.get("resultdate"),
            rv_result_date=result.get("rvresultdate"),
            reg_no=result.get("regno"),
            mc_no=result.get("mcnumber"),
            status=result.get("class"),
        )
        for result in response.json().get("data")
    ]


def parse_results_details(response: httpx.Response) -> Result:
    data = response.json()
    if response.status_code != 200:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Fetching User Profile with {response.status_code}"
        )
    return Result(
        student_details=StudentDetail(
            sem=response.json().get("studDet").get("FEXAMNAME"),
            full_sem=response.json().get("studDet").get("FDESCPN"),
            exam_date=response.json().get("studDet").get("FRESEXAMDATE"),
            exam_no=response.json().get("studDet").get("FEXAMNO"),
        ),
        result=ResultInfo(
            result=response.json().get("body")[0].get("result"),
            cgpa=response.json().get("body")[0].get("FCGPA"),
            sgpa=response.json().get("body")[0].get("FSGPA"),
            percentage=response.json().get("body")[0].get("FPERCENT"),
        ),
        subjects=[
            SubjectResult(
                id=sub_result.get("sl_no"),
                sub=sub_result.get("subject"),
                exam_type=sub_result.get("mthprue"),
                ese_marks=sub_result.get("uni_exam"),
                viva_marks=sub_result.get("viva_exam"),
                ia_marks=sub_result.get("ia_exam"),
                total_marks=sub_result.get("thtot"),
                credits=sub_result.get("FCREDITS"),
                grade_points=sub_result.get("FGP"),
                credit_points=sub_result.get("FCP"),
                remarks=sub_result.get("remarks1"),
                grade=sub_result.get("remarks"),
            )
            for sub_result in response.json().get("body")
        ],
    )
