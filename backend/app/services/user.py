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


async def verify_password(
    current_password: str,
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    return await client.post(
        url=MainUrls.PASSWORD,
        params={"action": "chkUser"},
        headers=authenticated_headers(token.credentials),
        data={"passwd": current_password},
    )


async def update_password(
    updated_password: str,
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    return await client.post(
        url=MainUrls.PASSWORD,
        params={"action": "updatePassword"},
        headers=authenticated_headers(token.credentials),
        data={"passwd": updated_password},
    )
