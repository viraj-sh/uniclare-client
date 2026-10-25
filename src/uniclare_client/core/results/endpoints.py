import httpx

from uniclare_client.core.clients.http import HttpClient
from uniclare_client.core.constants import MAIN_REFERER, build_headers
from uniclare_client.core.results.constants import (
    RESULTS_LIST_PARAMS,
    RESULTS_PATH,
)


async def list_results(http: HttpClient, session_token: str) -> httpx.Response:
    return await http.request(
        "GET",
        RESULTS_PATH,
        params=RESULTS_LIST_PARAMS,
        headers=build_headers(
            base_url=http.base_url,
            session_token=session_token,
            referer_path=MAIN_REFERER,
        ),
    )


async def result_details(
    http: HttpClient,
    *,
    exam_no: str,
    reg_no: str,
    session_token: str,
) -> httpx.Response:
    return await http.request(
        "GET",
        RESULTS_PATH,
        params={"a": "getResults", "examno": exam_no, "regno": reg_no},
        headers=build_headers(
            base_url=http.base_url,
            session_token=session_token,
            referer_path=MAIN_REFERER,
        ),
    )
