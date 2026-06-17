from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.http import HTTPClientDep, security
from app.core.urls import UserUrls
from app.core.constants import authenticated_headers


async def result_list(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    return await client.get(
        url=UserUrls.RESULT_LIST,
        params={"a": "getResAll"},
        headers=authenticated_headers(token.credentials),
    )


async def result(
    exam_no: str,
    reg_no: str,
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    client: HTTPClientDep,
):
    return await client.get(
        url=UserUrls.RESULT,
        params={"a": "getResults", "examno": f"{exam_no}", "regno": f"{reg_no}"},
        headers=authenticated_headers(token.credentials),
    )
