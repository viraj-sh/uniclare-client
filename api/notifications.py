from typing import Any, Dict
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from core.utils import standard_response
from core.logging import setup_logging
from core.exceptions import handle_exception
from services.notifications import fetch_notifications
from schema.pydantic_notification import (
    FetchNotificationsRequest,
    StandardResponseModel,
)

router = APIRouter(tags=["Notifications"])

logger = setup_logging(name="core.notification_endpoint", level="INFO")


@router.get(
    "/notification",
    operation_id="get_notifications",
    response_model=StandardResponseModel,
    responses={
        200: {"description": "Successful response with notifications"},
        400: {
            "description": "Client error, e.g. missing session or malformed upstream response"
        },
        401: {"description": "Unauthorized / invalid session"},
        500: {"description": "Internal server error"},
    },
)
def get_notifications(
    refetch: bool = Query(
        default=False,
        alias="refetch",
    )
) -> JSONResponse:

    try:
        logger.info(f"[NotificationEndpoint] Received request: refetch={refetch}")

        result: Dict[str, Any] = fetch_notifications(refetch=refetch)

        try:
            logger.info(
                f"[NotificationEndpoint] fetch_notifications result: success={result.get('success')} "
                f"status_code={result.get('status_code')}"
            )
        except Exception:
            logger.warning(
                "[NotificationEndpoint] Unable to parse fetch_notifications result for logging."
            )

        status_code = int(result.get("status_code", 200))
        return JSONResponse(content=result, status_code=status_code)

    except Exception as exc:
        err = handle_exception(logger, exc, context="get_notifications")
        if isinstance(err, dict):
            return JSONResponse(content=err, status_code=err.get("status_code", 500))
        return JSONResponse(
            content=standard_response(
                False, error_msg="Internal server error", status_code=500
            ),
            status_code=500,
        )
