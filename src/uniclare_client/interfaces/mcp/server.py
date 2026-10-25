# interfaces/mcp/server.py
from contextlib import asynccontextmanager

from fastmcp import FastMCP

from uniclare_client.core.api import App
from uniclare_client.core.errors import AppNotStarted

mcp = FastMCP("Uniclare MCP")

_app: App | None = None


def _get_app() -> App:
    if _app is None:
        raise AppNotStarted("MCP server not started")
    return _app


@asynccontextmanager
async def lifespan(server: FastMCP):
    global _app
    async with App() as app:
        _app = app
        try:
            yield
        finally:
            _app = None


mcp = FastMCP("Uniclare MCP", lifespan=lifespan)


@mcp.tool()
async def health() -> str:
    """Report the health status of the Uniclare MCP server."""
    status = await _get_app().health()
    if all(status.values()):
        return "Healthy"
    down = ", ".join(k for k, ok in status.items() if not ok)
    return f"Unhealthy: {down}"


def main(host: str = "127.0.0.1", port: int = 8000) -> None:
    try:
        mcp.run(transport="http", host=host, port=port)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
