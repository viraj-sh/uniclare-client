from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.core.urls import UserUrls
from app.core.constants import authenticated_headers


async def notification(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    return await client.get(
        url=UserUrls.NOTIFICATION, headers=authenticated_headers(token.credentials)
    )
