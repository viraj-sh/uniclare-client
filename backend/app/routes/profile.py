from fastapi import APIRouter, status, HTTPException, Depends
import httpx
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.services.profile import profile
from app.schemas.user import (
    UserResponse,
)

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def fetch_profile(
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
