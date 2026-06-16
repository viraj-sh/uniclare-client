from typing import List, Optional

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    full_name: Optional[str] = Field(None)
    fat_name: Optional[str] = Field(None)
    mot_name: Optional[str] = Field(None)
    degree_code: Optional[str] = Field(None)
    degree: Optional[str] = Field(None)
    college: Optional[str] = Field(None)
    college_code: Optional[str] = Field(None)
    photo: Optional[str] = Field(None)
    category: Optional[str] = Field(None)
    fee_type: Optional[str] = Field(None)
    reg_no: Optional[str] = Field(None)
    mob_no: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    parent_mob_no: Optional[str] = Field(None)


class NotificationResponse(BaseModel):
    title: Optional[str] = Field(None)
    body: Optional[str] = Field(None)
    date: Optional[str] = Field(None)


class ResultListResponse(BaseModel):
    year: Optional[str] = Field(None)
    exam_date: Optional[str] = Field(None)
    exam_name: Optional[str] = Field(None)
    result_date: Optional[str] = Field(None)
    rv_result_date: Optional[str] = Field(None)
    reg_no: Optional[str] = Field(None)
    mc_no: Optional[str] = Field(None)
    status: Optional[str] = Field(None)


class SubjectResult(BaseModel):
    id: Optional[int] = None
    sub: Optional[str] = None
    exam_type: Optional[str] = None
    ese_marks: Optional[str] = None
    viva_marks: Optional[str] = None
    ia_marks: Optional[str] = None
    total_marks: Optional[str] = None
    credits: Optional[str] = None
    grade_points: Optional[str] = None
    credit_points: Optional[str] = None
    remarks: Optional[str] = None
    grade: Optional[str] = None


class StudentDetail(BaseModel):
    sem: Optional[str] = None
    full_sem: Optional[str] = None
    exam_date: Optional[str] = None
    exam_no: Optional[str] = None


class ResultResponse(BaseModel):
    student_details: StudentDetail
    subjects: List[SubjectResult]
