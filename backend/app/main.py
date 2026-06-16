from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

from app.core.http import http_state
from app.core.config import settings
from app.routes import system


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    http_state.client = httpx.AsyncClient()
    yield
    # Shutdown
    await http_state.client.aclose()


app = FastAPI(
    title="unofficial pw-client api",
    description="view end-sem marks and detailed performance data that are hidden in uniclare app; includes mcp server for llm integration.",
    version=settings.version,
    lifespan=lifespan,
)

app.include_router(router=system.router, prefix="", tags=["system"])
