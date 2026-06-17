from typing import Optional

from pydantic import BaseModel, Field


class NotificationResponse(BaseModel):
    title: Optional[str] = Field(None)
    body: Optional[str] = Field(None)
    date: Optional[str] = Field(None)
