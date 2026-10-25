from uniclare_client.core.clients.http import HttpClient
from uniclare_client.core.results import endpoints, parsers
from uniclare_client.core.results.schema import Result, ResultSummary


class ResultsService:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    async def list(self, session_token: str) -> list[ResultSummary]:
        return parsers.parse_results_list(
            await endpoints.list_results(self._http, session_token)
        )

    async def details(
        self,
        *,
        exam_no: str,
        reg_no: str,
        session_token: str,
    ) -> Result:
        return parsers.parse_results_details(
            await endpoints.result_details(
                self._http,
                exam_no=exam_no,
                reg_no=reg_no,
                session_token=session_token,
            )
        )
