from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.http import http_state
from app.core.config import settings
from app.routes import notifications, system, auth, result, user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    http_state.client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=5.0,
            read=150.0,
            write=150.0,
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
    title="unofficial uniclare-client api",
    description="view end-sem marks and detailed performance data that are hidden in uniclare app; includes mcp server for llm integration.",
    version=settings.version,
    lifespan=lifespan,
)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=system.router, prefix="", tags=["system"])
app.include_router(router=auth.router, prefix="/auth", tags=["auth"])
app.include_router(router=user.router, prefix="/user", tags=["user"])
app.include_router(router=result.router, prefix="/result", tags=["result"])
app.include_router(
    router=notifications.router, prefix="/notifications", tags=["notifications"]
)
