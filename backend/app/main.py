from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

from app.core.http import http_state
from app.core.config import settings
from app.routes import system, auth, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    http_state.client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=5.0,
            read=50.0,
            write=10.0,
            pool=5.0,
        ),
        limits=httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20,
        ),
        follow_redirects=True,
    )
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
app.include_router(router=auth.router, prefix="/auth", tags=["auth"])
app.include_router(router=user.router, prefix="/user", tags=["user"])
