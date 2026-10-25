from pydantic import BaseModel, ConfigDict


class Notification(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    title: str
    body: str | None = None
    date: str | None = None
