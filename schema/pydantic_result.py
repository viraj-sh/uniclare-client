from __future__ import annotations
from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field


class StudentResultModel(BaseModel):
    year_id: Optional[str] = Field(None)
    exam_date: Optional[str] = Field(None)
    sem: Optional[str] = Field(None)
    result_date: Optional[str] = Field(None)
    reg_no: Optional[str] = Field(None)
    full_name: Optional[str] = Field(None)
    degree_id: Optional[str] = Field(None)
    degree_name: Optional[str] = Field(None)
    coll_id: Optional[str] = Field(None)
    coll_name: Optional[str] = Field(None)
    mc_no: Optional[str] = Field(None)
    status: Optional[str] = Field(None)

    model_config = {"from_attributes": True, "validate_by_name": True}


class ResultsQueryParams(BaseModel):
    refetch: bool = Field(False)


class StandardResponseModel(BaseModel):
    success: bool
    error: Optional[Any] = None
    data: Optional[Any] = None
    status_code: int

    model_config = {"from_attributes": True}


class ResultsListResponse(StandardResponseModel):
    data: Optional[List[StudentResultModel]] = None


class SubjectResultModel(BaseModel):
    no: int = Field(...)
    sub: str = Field("")
    remarks: str = Field("")
    type: str = Field("")
    end_marks: str = Field("")
    viva_marks: str = Field("")
    ia_marks: str = Field("")
    total_marks: str = Field("")
    credit_hrs: str = Field("")
    grade_points: str = Field("")
    credit_points: str = Field("")
    grade: str = Field("")


class ExamResultModel(BaseModel):
    full_sem: str = Field(...)
    sem: str = Field(...)
    col_name: str = Field(...)
    exam_date: str = Field(...)
    reg_no: str = Field(...)
    full_name: str = Field(...)
    result_date: Optional[str] = Field(None)
    rv_date: Optional[str] = Field(None)
    rt_date: Optional[str] = Field(None)
    pc_date: Optional[str] = Field(None)
    total_credits: Optional[str] = Field(None)
    sgpa: Optional[str] = Field(None)
    cgpa: Optional[str] = Field(None)
    percentage: Optional[str] = Field(None)
    result: Optional[str] = Field(None)
    subjects: List[SubjectResultModel] = Field(default_factory=list)


class FetchExamRequestModel(BaseModel):
    refetch: bool = Field(False)


class StandardResponseModel1(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[ExamResultModel] = Field(None)
    status_code: int = Field(...)


class ExamDetailModel(BaseModel):
    exam_type: Optional[str] = Field("")
    remark: Optional[str] = Field("")
    type: Optional[str] = Field("")


class SubjectItemModel(BaseModel):
    sub_name: str = Field(...)
    exams: Dict[str, ExamDetailModel] = Field(default_factory=dict)


class DataModel(BaseModel):
    subjects: List[SubjectItemModel] = Field(default_factory=list)


class StandardResponseModel2(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[DataModel] = Field(None)
    status_code: int = Field(...)
