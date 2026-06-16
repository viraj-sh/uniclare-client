from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.config import settings

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def root_endpoint():
    return JSONResponse(
        {
            "name": "uniclare-client-api",
            "version": settings.version,
            "docs_url": "https://github.com/viraj-sh/uniclare-client",
        }
    )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse({"status": "healthy"})
