from typing import Optional

from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    session_id: Optional[str] = Field(None)
    msg: Optional[str] = Field(None)
