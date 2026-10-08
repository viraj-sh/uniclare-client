import httpx

from app.clients.http import get_http_client
from app.results.endpoints import results_details, results_list
from app.results.parsers import parse_results_details, parse_results_list
from app.results.schemas import Result, ResultListResult


async def list_result(session_token: str) -> list[ResultListResult]:
    client = await get_http_client()
    try:
        response = await results_list(session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_results_list(response)


async def result_det(exam_no: str, reg_no: str, session_token: str) -> Result:
    client = await get_http_client()
    try:
        response = await results_details(exam_no, reg_no, session_token, client)

    except httpx.TimeoutException:
        raise TimeoutError("External API timed out")
    except httpx.NetworkError:
        raise ConnectionError("Could not reach external API")

    return parse_results_details(response)
