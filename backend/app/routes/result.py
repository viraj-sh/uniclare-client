from fastapi import APIRouter, status, HTTPException, Depends
import httpx
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.services.result import result_list, result
from app.schemas.result import (
    ResultListResponse,
    StudentDetail,
    SubjectResult,
    ResultResponse,
    ResultInfo,
)

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def fetch_result_list(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    try:
        response = await result_list(token, client)

        if response.status_code == 200:
            return [
                ResultListResponse(
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
        return response.json()
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(504, "External API timed out")
    except httpx.NetworkError:
        raise HTTPException(502, "Could not reach external API")
    except Exception as exc:
        raise HTTPException(500, f"Unexpected error: {exc}")


@router.get("/{exam_no}", status_code=status.HTTP_200_OK)
async def fetch_result(
    exam_no: str,
    reg_no: str,
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    try:
        response = await result(exam_no, reg_no, token, client)

        if response.status_code == 200:
            return ResultResponse(
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
        return response.json()
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(504, "External API timed out")
    except httpx.NetworkError:
        raise HTTPException(502, "Could not reach external API")
    except Exception as exc:
        raise HTTPException(500, f"Unexpected error: {exc}")
