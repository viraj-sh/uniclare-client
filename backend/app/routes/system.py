from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import time

from app.core.config import settings

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def root_endpoint():
    start_time = time.perf_counter()
    print(
        f"[root_endpoint]: Time -> {(time.perf_counter() - start_time) * 1000:.3f}ms | Cache -> {False}"
    )
    return JSONResponse(
        {
            "name": "uniclare-client-api",
            "version": settings.version,
            "docs_url": "https://github.com/viraj-sh/uniclare-client",
        }
    )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    start_time = time.perf_counter()
    print(
        f"[health_check]: Time -> {(time.perf_counter() - start_time) * 1000:.3f}ms | Cache -> {False}"
    )
    return JSONResponse({"status": "healthy"})
