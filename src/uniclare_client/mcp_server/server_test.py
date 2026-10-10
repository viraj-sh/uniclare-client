from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token

from uniclare_client.core.api import app
from uniclare_client.core.lifecycle import shutdown, startup
from uniclare_client.mcp_server.auth_test import (
    complete_handler,
    connect_info_handler,
    provider,
)


@asynccontextmanager
async def lifespan(server: FastMCP):
    await startup()
    try:
        yield
    finally:
        await shutdown()


mcp = FastMCP("Uniclare MCP", auth=provider, lifespan=lifespan)
mcp.custom_route("/connect-info", methods=["GET", "OPTIONS"])(connect_info_handler)
mcp.custom_route("/complete", methods=["POST", "OPTIONS"])(complete_handler)
# mcp.custom_route("/login", methods=["GET", "POST"])(login_handler) # main


def _token() -> str:
    access = get_access_token()
    if access is None:
        raise PermissionError("Unauthenticated")
    return access.token


@mcp.tool()
async def fetch_profile():
    """Fetch the current student's profile details."""
    return await app.profile(_token())


@mcp.tool()
async def fetch_notifications():
    """Fetch the current student's notifications."""
    return await app.notifications(_token())


@mcp.tool()
async def fetch_results_list():
    """Fetch a list of the current student's results with summary details (title, semester, pass/fail, etc.)."""
    return await app.results_list(_token())


@mcp.tool()
async def fetch_result_deatails(
    exam_no: str,
    reg_no: str,
):
    """Fetch the complete details of a specific exam result.

    Args:
        exam_no: Exam number identifying which exam result to view in detail.
            Get this from `fetch_results_list`.
        reg_no: Student registration number. Get this from `fetch_profile`.
    """
    return await app.result_details(exam_no, reg_no, _token())


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
