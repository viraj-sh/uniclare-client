from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, RootModel


class NotificationModel(RootModel[Dict[str, Any]]):

    root: Dict[str, Any] = Field(default_factory=dict)


class FetchNotificationsRequest(BaseModel):

    refetch: Optional[bool] = Field(default=False)


class StandardResponseModel(BaseModel):

    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[Any] = Field(None)
    status_code: int = Field(...)


class NotificationsDataModel(BaseModel):

    notifications: List[Dict[str, Any]] = Field(default_factory=list)
