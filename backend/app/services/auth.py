from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.core.urls import AuthUrls
from app.core.constants import authenticated_headers, unauthenticated_headers


async def otp(mob_no: str, client: HTTPClientDep):
    return await client.post(url=AuthUrls.OTP, data={"mobile": mob_no})


async def reset_password(
    mob_no: str, otp: str, new_password: str, client: HTTPClientDep
):
    return await client.post(
        url=AuthUrls.RESET_PASSWORD,
        data={"mobile": mob_no, "otp": otp, "password": new_password},
    )


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
