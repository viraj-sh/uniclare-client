from pydantic import BaseModel, ConfigDict


class ResultSummary(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    year: str
    exam_name: str
    exam_date: str | None = None
    result_date: str | None = None
    rv_result_date: str | None = None
    reg_no: str
    mc_no: str | None = None
    status: str | None = None  # vendor calls it "class" — renamed to domain term


class StudentDetail(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    sem: str | None = None
    full_sem: str | None = None
    exam_date: str | None = None
    exam_no: str


class ResultInfo(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    result: str | None = None
    cgpa: str | None = None
    sgpa: str | None = None
    percentage: str | None = None


class SubjectResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    id: int | None = None
    sub: str | None = None
    exam_type: str | None = None
    ese_marks: str | None = None
    viva_marks: str | None = None
    ia_marks: str | None = None
    total_marks: str | None = None
    credits: str | None = None
    grade_points: str | None = None
    credit_points: str | None = None
    remarks: str | None = None
    grade: str | None = None


class Result(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    student_details: StudentDetail
    result: ResultInfo
    subjects: list[SubjectResult]
