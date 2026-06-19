from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
import httpx
import time
from typing import Annotated

from app.core.http import HTTPClientDep, security
from app.services.auth import signin, signout, otp, reset_password
from app.schemas.auth import LoginResponse
from app.core.utils import extract_json

router = APIRouter()


@router.post("/send-otp", status_code=status.HTTP_200_OK)
async def send_password_reset_otp(mobile_no: str, client: HTTPClientDep):
    start_time = time.perf_counter()
    try:
        response = await otp(mobile_no, client)
        print(
            f"[send_password_reset_otp]: Time -> {(time.perf_counter() - start_time) * 1000:.3f}ms"
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


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password_using_otp(
    mobile_no: str, otp: str, new_password: str, client: HTTPClientDep
):
    start_time = time.perf_counter()
    try:
        response = await reset_password(mobile_no, otp, new_password, client)
        print(
            f"[reset_password_using_otp]: Time -> {(time.perf_counter() - start_time) * 1000:.3f}ms"
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


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(mobile_no: str, password: str, client: HTTPClientDep):
    start_time = time.perf_counter()
    try:
        response = await signin(mobile_no, password, client)
        data = extract_json(response.text)
        if response.status_code == 200:
            if response.cookies.get("PHPSESSID") is not None:
                print(
                    f"[user_login]: Time -> {(time.perf_counter() - start_time) * 1000:.3f}ms"
                )
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
    start_time = time.perf_counter()
    try:
        response = await signout(token, client)
        print(
            f"[user_logout]: Time -> {(time.perf_counter() - start_time) * 1000:.3f}ms"
        )
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(504, "External API timed out")
    except httpx.NetworkError:
        raise HTTPException(502, "Could not reach external API")
    except Exception as exc:
        raise HTTPException(500, f"Unexpected error: {exc}")
