# interfaces/mcp/server.py
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken, TokenVerifier
from fastmcp.server.dependencies import get_access_token

from uniclare_client.core.api import App
from uniclare_client.core.errors import AppNotStarted

mcp = FastMCP("Uniclare MCP")

_app: App | None = None


def _token() -> str:
    access = get_access_token()
    if access is None:
        raise PermissionError("Unauthenticated")
    return access.token


def _get_app() -> App:
    if _app is None:
        raise AppNotStarted("MCP server not started")
    return _app


class UniTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            app = _get_app()
        except AppNotStarted:
            return None
        if await app.auth.verify_session(token):
            return AccessToken(token=token, client_id="uniclare", scopes=[])
        return None


@asynccontextmanager
async def lifespan(server: FastMCP):
    global _app
    async with App() as app:
        _app = app
        try:
            yield
        finally:
            _app = None


mcp = FastMCP("Uniclare MCP", auth=UniTokenVerifier(), lifespan=lifespan)


@mcp.tool()
async def health() -> str:
    """Report the health status of the Uniclare MCP server."""
    status = await _get_app().health()
    if all(status.values()):
        return "Healthy"
    down = ", ".join(k for k, ok in status.items() if not ok)
    return f"Unhealthy: {down}"


@mcp.tool()
async def fetch_results_list() -> list[dict]:
    """Fetch a list of the current student's exam results, newest first.

    Each entry contains:
      - year: exam code to use with `fetch_result_details` (e.g. 'F-2026-1')
      - reg_no: registration number to use with `fetch_result_details`
      - exam_name, exam_date, result_date, status
    """
    summaries = await _get_app().results.list(_token())
    return [s.model_dump(mode="json") for s in summaries]


@mcp.tool()
async def fetch_result_details(exam_no: str, reg_no: str) -> dict:
    """Fetch the complete details of a specific exam result.

    Args:
        exam_no: Exam code from `fetch_results_list` — the `year` field of the
            desired entry (e.g. 'F-2026-1' for VI Semester, 'E-2025-2' for V Semester).
        reg_no: Registration number from `fetch_results_list` — the `reg_no`
            field of the same entry.
    """
    result = await _get_app().results.details(
        exam_no=exam_no,
        reg_no=reg_no,
        session_token=_token(),
    )
    return result.model_dump(mode="json")


def main(host: str = "127.0.0.1", port: int = 8000) -> None:
    try:
        mcp.run(transport="http", host=host, port=port)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
