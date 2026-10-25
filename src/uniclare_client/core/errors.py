from typing import Any


class AppError(Exception):
    code = "app_error"

    def __init__(
        self, message: str | None = None, *, details: dict[str, Any] | None = None
    ) -> None:
        self.message = message or self.code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


class AppNotStarted(AppError):
    code = "app_not_started"


class ConfigError(AppError):
    code = "config_error"


class NotFound(AppError):
    code = "not_found"


class InvalidInput(AppError):
    code = "invalid_input"


class ExternalAPIError(AppError):
    code = "external_error"


class ExternalTimeout(ExternalAPIError):
    code = "external_timeout"


class ExternalUnavailable(ExternalAPIError):
    code = "external_unavailable"


class RateLimited(ExternalAPIError):
    code = "rate_limited"


class InvalidResponse(ExternalAPIError):
    code = "invalid_response"


class AuthenticationError(AppError):
    code = "authentication_error"


class InvalidCredentials(AuthenticationError):
    code = "invalid_credentials"


class SessionExpired(AuthenticationError):
    code = "session_expired"
