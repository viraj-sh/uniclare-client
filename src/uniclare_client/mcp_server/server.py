from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken, TokenVerifier
from fastmcp.server.dependencies import get_access_token

from uniclare_client.core.api import app
from uniclare_client.core.lifecycle import shutdown, startup


class UniTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        result = await app.verify_session_token(token)
        if result.status != "success" or result.error_code != 0:
            return None
        return AccessToken(token=token, client_id="uniclare", scopes=[])


@asynccontextmanager
async def lifespan(server: FastMCP):
    await startup()
    try:
        yield
    finally:
        await shutdown()


mcp = FastMCP("Uniclare MCP", auth=UniTokenVerifier(), lifespan=lifespan)


def _token() -> str:
    access = get_access_token()
    if access is None:
        raise PermissionError("Unauthenticated")
    return access.token


@mcp.tool()
async def fetch_profile():
    """Fetch the current student's profile details."""
    profile = await app.profile(_token())
    return profile


@mcp.tool()
async def fetch_notifications():
    """Fetch the current student's notifications."""
    notifications = await app.notifications(_token())
    return notifications


@mcp.tool()
async def fetch_results_list():
    """Fetch a list of the current student's results with summary details (title, semester, pass/fail, etc.)."""
    results_list = await app.results_list(_token())
    return results_list


@mcp.tool()
async def fetch_result_deatails(
    exam_no: str,
    reg_no: str,
):
    """Fetch the complete details of a specific exam result.

    Args:
        exam_no: Exam number identifying which exam result to view in detail.
            This is the `year` value returned by `fetch_results_list`
            (e.g., 'F-2026-1' for VI Semester, 'E-2025-2' for V Semester, etc.).
            Get this from `fetch_results_list` by reading the `year` field of the
            desired result entry.
        reg_no: Student registration number. Get this from `fetch_profile`.
    """
    result_details = await app.result_details(exam_no, reg_no, _token())
    return result_details


def main():
    mcp.run(transport="http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
