from fastapi import APIRouter, Query, Path
from fastapi.responses import JSONResponse
from core.utils import standard_response
from core.logging import setup_logging
from core.exceptions import handle_exception
from services.result import (
    fetch_student_results,
    fetch_exam_result,
    fetch_detailed_exam_result,
)
from schema.pydantic_result import (
    ResultsListResponse,
    ResultsQueryParams,
    StandardResponseModel1,
    StandardResponseModel2,
)

logger = setup_logging(name="api.result")

router = APIRouter(tags=["Result"])


@router.get(
    "/results",
    response_model=ResultsListResponse,
    operation_id="get_student_results",
    summary="Fetch summary list of all student exam results",
)
async def get_results(refetch: bool = Query(False, title="Refetch")) -> JSONResponse:
    try:
        request_params = ResultsQueryParams(refetch=refetch)
        result = fetch_student_results(refetch=request_params.refetch)
        return JSONResponse(content=result, status_code=result.get("status_code", 200))
    except Exception as exc:
        handled = handle_exception(logger, exc, context="results_endpoint")
        return JSONResponse(
            content=handled, status_code=handled.get("status_code", 500)
        )


@router.get(
    "/results/{exam_code}",
    response_model=StandardResponseModel1,
    operation_id="fetchExamResult",
    summary="Fetch detailed exam result for a given exam code",
)
async def get_exam_result(
    exam_code: str = Path(...),
    refetch: bool = Query(False),
) -> JSONResponse:
    try:
        result = fetch_exam_result(exam_code=exam_code, refetch=refetch)
        return JSONResponse(content=result, status_code=result.get("status_code", 200))
    except Exception as exc:
        handled = handle_exception(logger, exc, context="fetch_exam_result_endpoint")
        return JSONResponse(
            content=handled, status_code=handled.get("status_code", 500)
        )


@router.get(
    "/results/{exam_code}/detailed",
    response_model=StandardResponseModel2,
    operation_id="get_detailed_exam_results",
    summary="Fetch very detailed exam result by exam code",
)
async def get_detailed_exam_result(
    exam_code: str = Path(...),
    refetch: bool = Query(False),
):
    try:
        if not exam_code or not exam_code.strip():
            result = standard_response(
                success=False, error="exam_code is required", status_code=400
            )
            return JSONResponse(
                content=result, status_code=result.get("status_code", 400)
            )

        result = fetch_detailed_exam_result(exam_code=exam_code, refetch=refetch)

        if not isinstance(result, dict):
            logger.error(
                "fetch_detailed_exam_result returned non-dict: %r", type(result)
            )
            result = standard_response(
                success=False, error="Internal error", status_code=500
            )

        status_code = int(result.get("status_code", 200))

        return JSONResponse(content=result, status_code=status_code)

    except Exception as exc:
        handled = handle_exception(logger, exc, context="get_detailed_exam_result")
        if isinstance(handled, dict):
            return JSONResponse(
                content=handled, status_code=int(handled.get("status_code", 500))
            )
        return handled
