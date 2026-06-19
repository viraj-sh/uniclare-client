from fastapi import APIRouter, status, HTTPException, Depends
import httpx
import time
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.services.notifications import notification
from app.schemas.notification import (
    NotificationResponse,
)

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def fetch_notifications(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    start_time = time.perf_counter()
    try:
        response = await notification(token, client)

        if response.status_code == 200:
            data = response.json()
            print(
                f"[fetch_notifications]: Time -> {(time.perf_counter() - start_time) * 1000:.3f}ms"
            )
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
