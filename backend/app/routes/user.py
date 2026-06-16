from fastapi import APIRouter, status, HTTPException, Depends
import httpx
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.services.user import profile, notification, result_list
from app.schemas.user import UserResponse, NotificationResponse, ResultListResponse

router = APIRouter()


@router.post("/profile", status_code=status.HTTP_200_OK)
async def user_login(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    try:
        response = await profile(token, client)

        if response.status_code == 200:
            data = response.json()
            return UserResponse(
                full_name=data.get("fname"),
                fat_name=data.get("ffatname"),
                mot_name=data.get("fmotname"),
                degree=data.get("fdegree"),
                degree_code=data.get("fdeggrp"),
                college=data.get("college"),
                college_code=data.get("fcollcode"),
                photo=data.get("photo"),
                category=data.get("category"),
                fee_type=data.get("feetype"),
                reg_no=data.get("strRegno"),
                mob_no=data.get("strMobile"),
                email=data.get("strEmail"),
                parent_mob_no=data.get("strParentMob"),
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


@router.get("/notifications", status_code=status.HTTP_200_OK)
async def user_notifications(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    try:
        response = await notification(token, client)

        if response.status_code == 200:
            data = response.json()
            return [
                NotificationResponse(
                    title=noti.get("ftitle"),
                    body=noti.get("fbody"),
                    date=noti.get("fpushdate"),
                )
                for noti in data
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


@router.get("/result-list", status_code=status.HTTP_200_OK)
async def user_result_list(
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
