from app.core.http import HTTPClientDep
from app.core.urls import AuthUrls
from app.core.constants import unauthenticated_headers


async def signin(mob_no: str, password: str, client: HTTPClientDep):
    payload = {"regno": mob_no, "passwd": password}
    return await client.post(
        url=AuthUrls.SIGNIN, headers=unauthenticated_headers(), data=payload
    )
