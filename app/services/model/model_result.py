from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict, List
import re


@dataclass
class StudentResult:
    year_id: Optional[str]
    exam_date: Optional[str]
    sem: Optional[str]
    result_date: Optional[str]
    reg_no: Optional[str]
    full_name: Optional[str]
    degree_id: Optional[str]
    degree_name: Optional[str]
    coll_id: Optional[str]
    coll_name: Optional[str]
    mc_no: Optional[str]
    status: Optional[str]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional["StudentResult"]:
        if not isinstance(data, dict):
            return None

        try:
            college_parts = (data.get("college") or "").split(" - ", 1)
            coll_id = college_parts[0].strip() if len(college_parts) > 0 else ""
            coll_name = college_parts[1].strip() if len(college_parts) > 1 else ""

            degree_parts = (data.get("degree") or "").split(" - ", 1)
            degree_id = degree_parts[0].strip() if len(degree_parts) > 0 else ""
            degree_name = degree_parts[1].strip() if len(degree_parts) > 1 else ""

            return cls(
                year_id=data.get("year"),
                exam_date=data.get("examdate"),
                sem=data.get("examname"),
                result_date=data.get("resultdate"),
                reg_no=data.get("regno"),
                full_name=data.get("name"),
                degree_id=degree_id,
                degree_name=degree_name,
                coll_id=coll_id,
                coll_name=coll_name,
                mc_no=data.get("mcnumber"),
                status=data.get("class"),
            )
        except Exception:
            return None


@dataclass
class SubjectResult:
    no: int
    sub: str
    remarks: str
    type: str
    end_marks: str
    viva_marks: str
    ia_marks: str
    total_marks: str
    credit_hrs: str
    grade_points: str
    credit_points: str
    grade: str


@dataclass
class ExamResult:
    full_sem: str
    sem: str
    col_name: str
    exam_date: str
    reg_no: str
    full_name: str
    result_date: Optional[str]
    rv_date: Optional[str]
    rt_date: Optional[str]
    pc_date: Optional[str]
    total_credits: Optional[str]
    sgpa: Optional[str]
    cgpa: Optional[str]
    percentage: Optional[str]
    result: Optional[str]
    subjects: List[SubjectResult]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional["ExamResult"]:
        try:
            if "studDet" not in data or "body" not in data:
                return None

            stud = data.get("studDet", {})
            body = data.get("body", [])
            dates = data.get("dates", {})
            ecredits = data.get("ecredits", "")

            required_stud_fields = [
                "FDESCPN",
                "FEXAMNAME",
                "FCOLLNAME",
                "FRESEXAMDATE",
                "FREGNO",
                "FNAME",
            ]
            if not all(field in stud for field in required_stud_fields):
                return None

            full_sem = stud.get("FDESCPN")
            sem = stud.get("FEXAMNAME")
            col_name = stud.get("FCOLLNAME")
            exam_date = stud.get("FRESEXAMDATE")
            reg_no = stud.get("FREGNO")
            full_name = stud.get("FNAME")

            sgpa = body[0].get("FSGPA") if body else None
            cgpa = body[0].get("FCGPA") if body else None
            percentage = body[0].get("FPERCENT") if body else None
            result_status = body[0].get("result") if body else None

            subjects: List[SubjectResult] = []
            for row in body:
                subject = SubjectResult(
                    no=row.get("sl_no", 0),
                    sub=row.get("subject", ""),
                    remarks=row.get("remarks1", ""),
                    type=row.get("mthprue", ""),
                    end_marks=row.get("uni_exam", ""),
                    viva_marks=row.get("viva_exam", ""),
                    ia_marks=row.get("ia_exam", ""),
                    total_marks=row.get("thtot", ""),
                    credit_hrs=row.get("FCREDITS", ""),
                    grade_points=row.get("FGP", ""),
                    credit_points=row.get("FCP", ""),
                    grade=row.get("remarks", ""),
                )
                subjects.append(subject)

            result_date = dates.get("accDate")
            scroll_txt = dates.get("scroll_txt", "")
            matches = re.findall(r"(\d{2}/\d{2}/\d{4})", scroll_txt)
            rv_date = matches[0] if len(matches) > 0 else None
            rt_date = matches[1] if len(matches) > 1 else None
            pc_date = matches[2] if len(matches) > 2 else None

            credits_match = re.search(r":\s*(\d+)", ecredits)
            credits = credits_match.group(1) if credits_match else None

            return cls(
                full_sem=full_sem,
                sem=sem,
                col_name=col_name,
                exam_date=exam_date,
                reg_no=reg_no,
                full_name=full_name,
                result_date=result_date,
                rv_date=rv_date,
                rt_date=rt_date,
                pc_date=pc_date,
                total_credits=credits,
                sgpa=sgpa,
                cgpa=cgpa,
                percentage=percentage,
                result=result_status,
                subjects=subjects,
            )

        except Exception:
            return None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExamDetail:
    exam_type: str
    remark: str
    type: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional["ExamDetail"]:
        try:
            return cls(
                exam_type=data.get("s", ""),
                remark=data.get("m", ""),
                type=data.get("thpr", ""),
            )
        except Exception:
            return None


@dataclass
class SubjectsResult:
    sub_name: str
    exams: Dict[str, ExamDetail]

    @classmethod
    def from_json(
        cls, sub_name: str, data: Dict[str, Any]
    ) -> Optional["SubjectResult"]:
        try:
            exams = {}
            for exam_code, exam_info in data.items():
                exam_detail = ExamDetail.from_json(exam_info)
                if exam_detail is None:
                    continue
                exams[exam_code] = exam_detail
            if not exams:
                return None
            return cls(sub_name=sub_name, exams=exams)
        except Exception:
            return None
