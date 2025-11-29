from fastapi import APIRouter, Query, Body
from fastapi.responses import JSONResponse
from typing import Optional
from core.utils import standard_response
from core.logging import setup_logging
from core.exceptions import handle_exception
from schema.pydantic_profile import (
    ProfileRequestModel,
    StandardResponseModel,
    StandardResponse,
    EditableProfileData,
    EditableProfileRequest,
    ProfileEditRequest,
    StandardResponseModel2,
)
from services.profile import (
    fetch_profile,
    fetch_editable_profile,
    update_editable_profile,
)

logger = setup_logging(name="api.profile")

router = APIRouter(tags=["Profile"])


@router.get(
    "/profile",
    response_model=StandardResponseModel,
    operation_id="get_student_profile",
    summary="Fetch full student profile",
)
def get_profile(refetch: bool = Query(False)):
    try:
        request_payload = ProfileRequestModel(refetch=refetch)
        result = fetch_profile(refetch=request_payload.refetch)
        if not isinstance(result, dict):
            fallback = standard_response(
                False,
                error_msg="Unexpected response from fetch_profile",
                status_code=500,
            )
            return JSONResponse(
                content=fallback, status_code=fallback.get("status_code", 500)
            )
        return JSONResponse(content=result, status_code=result.get("status_code", 200))
    except Exception as exc:
        err = handle_exception(logger, exc, context="get_profile")
        if isinstance(err, dict):
            return JSONResponse(content=err, status_code=err.get("status_code", 500))
        fallback = standard_response(
            False, error_msg="Internal server error", status_code=500
        )
        return JSONResponse(
            content=fallback, status_code=fallback.get("status_code", 500)
        )


@router.get(
    "/profile/editable",
    response_model=StandardResponse,
    operation_id="get_editable_profile",
    summary="Fetch editable student profile fields",
)
async def get_editable_profile(refetch: bool = Query(False)) -> JSONResponse:
    try:
        req = EditableProfileRequest(refetch=refetch)
        result: Dict[str, Any] = fetch_editable_profile(refetch=req.refetch)

        if not isinstance(result, dict):
            resp = standard_response(
                False, error_msg="Unexpected response type", status_code=500
            )
            return JSONResponse(content=resp, status_code=500)

        status_code: int = int(result.get("status_code", 500))

        if not result.get("success", False):
            return JSONResponse(content=result, status_code=status_code)

        raw_data: Optional[Dict[str, Any]] = result.get("data")
        if not raw_data:
            resp = standard_response(
                False, error_msg="No profile data found", status_code=500
            )
            return JSONResponse(content=resp, status_code=500)

        filtered_data = {
            "reg_no": raw_data.get("reg_no"),
            "full_name": raw_data.get("full_name"),
            "fath_name": raw_data.get("fath_name"),
            "mot_name": raw_data.get("mot_name"),
            "abc_id": raw_data.get("abc_id"),
            "sphoto": raw_data.get("sphoto"),
        }

        profile_data = EditableProfileData(**filtered_data)

        resp = standard_response(True, error_msg=None, status_code=status_code)
        resp["data"] = profile_data.dict()

        return JSONResponse(content=resp, status_code=status_code)

    except Exception as exc:
        handled = handle_exception(logger, exc, context="get_editable_profile")
        return JSONResponse(
            content=handled, status_code=handled.get("status_code", 500)
        )


@router.patch(
    "/profile/edit",
    response_model=StandardResponseModel2,
    operation_id="update_editable_profile_patch",
    summary="Update editable profile fields",
)
async def edit_profile(payload: ProfileEditRequest = Body(...)) -> JSONResponse:
    try:
        result = update_editable_profile(
            ffatname=payload.father_name,
            fmotname=payload.mother_name,
            fabcno=payload.abc_no,
        )
        return JSONResponse(content=result, status_code=result.get("status_code", 200))
    except Exception as exc:
        return handle_exception(logger, exc, context="edit_profile")
