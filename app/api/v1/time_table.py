from fastapi import APIRouter, Query
from core.utils import standard_response
from core.logging import setup_logging
from core.exceptions import handle_exception
from fastapi.responses import JSONResponse
from typing import Optional
from schema.pydantic_timetable import (
    StandardResponseModel,
)
from services.time_table import fetch_practical_timetable

router = APIRouter(prefix="/timetable", tags=["Time Table"])

logger = setup_logging(name="core.routes.practical")


@router.get(
    "/practical",
    operation_id="get_practical_timetable",
    response_model=StandardResponseModel,
    responses={
        200: {
            "description": "Practical timetable retrieved (or appropriate standard_response)"
        },
        400: {"description": "Bad request or invalid session"},
        401: {"description": "Unauthorized / missing session"},
        500: {"description": "Internal server error"},
    },
)
async def get_practical_timetable(
    refetch: Optional[bool] = Query(
        False, description="Force refetch and invalidate cached result"
    ),
):
    logger.info("Incoming request to /practical with refetch=%s", refetch)
    try:
        result = fetch_practical_timetable(refetch=bool(refetch))

        if not isinstance(result, dict):
            fallback = standard_response(
                success=False,
                error="Internal: function returned invalid result type",
                status_code=500,
            )
            logger.error(
                "fetch_practical_timetable returned non-dict: %s", type(result)
            )
            return JSONResponse(
                content=fallback, status_code=fallback.get("status_code", 500)
            )

        status_code = result.get("status_code", 200)
        logger.info(
            "fetch_practical_timetable returned status_code=%s success=%s",
            status_code,
            result.get("success"),
        )
        return JSONResponse(content=result, status_code=status_code)

    except Exception as exc:
        logger.exception("Unhandled exception in endpoint /practical")
        err_resp = handle_exception(logger, exc, context="get_practical_timetable")
        if not isinstance(err_resp, dict):
            fallback = standard_response(
                success=False,
                error="Unhandled error while processing request",
                status_code=500,
            )
            return JSONResponse(
                content=fallback, status_code=fallback.get("status_code", 500)
            )
        return JSONResponse(
            content=err_resp, status_code=err_resp.get("status_code", 500)
        )
