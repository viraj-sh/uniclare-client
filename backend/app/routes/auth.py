from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
import httpx
from typing import Annotated

from app.core.http import HTTPClientDep, security
from app.services.auth import signin, signout
from app.schemas.auth import LoginResponse
from app.core.utils import extract_json

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(mobile_no: str, password: str, client: HTTPClientDep):
    try:
        response = await signin(mobile_no, password, client)
        data = extract_json(response.text)
        if response.status_code == 200 and data.get("error_code") == "0":
            if response.cookies.get("PHPSESSID") is not None:
                return LoginResponse(
                    session_id=response.cookies.get("PHPSESSID"), msg=data.get("msg")
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{data.get('error_code')} -> {data.get('msg')}",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{data.get('error_code')} -> {data.get('msg')}",
            )
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(504, "External API timed out")
    except httpx.NetworkError:
        raise HTTPException(502, "Could not reach external API")
    except Exception as exc:
        raise HTTPException(500, f"Unexpected error: {exc}")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def user_logout(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    try:
        await signout(token, client)

    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(504, "External API timed out")
    except httpx.NetworkError:
        raise HTTPException(502, "Could not reach external API")
    except Exception as exc:
        raise HTTPException(500, f"Unexpected error: {exc}")
