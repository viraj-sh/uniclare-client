from pydantic import BaseModel, Field
from typing import Optional, Any, Dict, List


class SubjectModel(BaseModel):
    code: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    exam_date: Optional[str] = Field(None)

    class Config:
        extra = "allow"


class PracticalDataModel(BaseModel):

    stud_name: Optional[str] = Field(None)
    degree_name: Optional[str] = Field(None)
    sem: Optional[str] = Field(None)
    reg_no: Optional[str] = Field(None)
    center_name: Optional[str] = Field(None)
    subjects: List[Dict[str, Any]] = Field(
        default_factory=list,
    )


class StandardResponseModel(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[PracticalDataModel] = Field(None)
    status_code: int = Field(...)

    class Config:
        arbitrary_types_allowed = True
