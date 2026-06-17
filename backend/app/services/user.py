from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.core.urls import MainUrls
from app.core.constants import authenticated_headers


async def profile(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):

    return await client.get(
        url=MainUrls.PROFILE, headers=authenticated_headers(token.credentials)
    )
