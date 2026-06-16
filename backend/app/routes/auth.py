from fastapi import APIRouter, status, HTTPException
import httpx

from app.core.http import HTTPClientDep
from app.services.auth import signin
from app.schemas.auth import LoginResponse
from app.core.utils import extract_json

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(mobile_no: str, password: str, client: HTTPClientDep):
    try:
        response = await signin(mobile_no, password, client)
        if response.status_code == 200:
            if response.cookies.get("PHPSESSID") is not None:
                data = extract_json(response.text)

                return LoginResponse(
                    session_id=response.cookies.get("PHPSESSID"), msg=data.get("msg")
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="invalid registration number or password",
                )
        return extract_json(response.text)
    except HTTPException:
        raise
    except httpx.TimeoutException:
        raise HTTPException(504, "External API timed out")
    except httpx.NetworkError:
        raise HTTPException(502, "Could not reach external API")
    except Exception as exc:
        raise HTTPException(500, f"Unexpected error: {exc}")
