from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.system import router as system_router
from api.profile import router as profile_router
from api.result import router as result_router
from api.auth import router as auth_router
from core.logging import setup_logging
from fastapi_mcp import FastApiMCP
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

logger = setup_logging(name="app", level="INFO")

app = FastAPI(title="Unofficial uniclare API")

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Application startup complete")

# Include routers
app.include_router(system_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(result_router, prefix="/api")

mcp = FastApiMCP(
    app,
    include_operations=[
        "check_system_health",
        "get_system_info",
        "auth_login_post",
        "auth_validate_session_get",
        "auth_logout_post",
        "auth_send_password_reset_otp_post",
        "password_reset_confirm_post",
        "get_student_profile",
        "get_editable_profile",
        "update_editable_profile_patch",
        "get_student_results",
        "fetchExamResult",
        "get_detailed_exam_results",
    ],
)
mcp.mount_http()

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
