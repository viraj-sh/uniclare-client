from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.core.urls import AuthUrls
from app.core.constants import authenticated_headers, unauthenticated_headers


async def signin(mob_no: str, password: str, client: HTTPClientDep):
    payload = {"regno": mob_no, "passwd": password}
    return await client.post(
        url=AuthUrls.SIGNIN, headers=unauthenticated_headers(), data=payload
    )


async def signout(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    return await client.post(
        url=AuthUrls.SIGNOUT, headers=authenticated_headers(token.credentials)
    )
