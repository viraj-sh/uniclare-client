from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
import httpx
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.http import http_state
from app.core.config import settings
from app.routes import notifications, system, auth, result, user
from app.core.utils import static_path


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

static_dir = static_path()

app.include_router(router=system.router, prefix="/api", tags=["system"])
app.include_router(router=auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(router=user.router, prefix="/api/user", tags=["user"])
app.include_router(router=result.router, prefix="/api/result", tags=["result"])
app.include_router(
    router=notifications.router, prefix="/api/notifications", tags=["notifications"]
)

# print(f"static_dir -> {static_dir} | exists? -> {os.path.isdir(static_dir)} | index.html exists? -> {os.path.isfile(os.path.join(static_dir, 'index.html'))}")

if os.path.isdir(static_dir) and os.path.isfile(os.path.join(static_dir, "index.html")):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        return FileResponse(os.path.join(static_dir, "index.html"))
