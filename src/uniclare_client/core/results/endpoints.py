import httpx

from uniclare_client.core.constants import API_BASE_URL
from uniclare_client.core.http_headers import authenticated_headers

RESULTS_LIST_URL = f"{API_BASE_URL}/src/results_new.php"
RESULTS_DETAILS_URL = f"{API_BASE_URL}/src/results_new.php"


async def results_list(session_token: str, client: httpx.AsyncClient):
    params = {"a": "getResAll"}
    return await client.get(
        url=RESULTS_LIST_URL,
        headers=authenticated_headers(session_token),
        params=params,
    )


async def results_details(
    exam_no: str, reg_no: str, session_token: str, client: httpx.AsyncClient
):
    params = {"a": "getResults", "examno": f"{exam_no}", "regno": f"{reg_no}"}
    return await client.get(
        url=RESULTS_DETAILS_URL,
        params=params,
        headers=authenticated_headers(session_token),
    )
