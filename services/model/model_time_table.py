from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class PracticalSubject:
    sub_code: Optional[str]
    sub_name: Optional[str]
    exam_date: Optional[str]
    exam_no: Optional[str]
    batch: Optional[str]
    exam_time: Optional[str]


@dataclass
class PracticalTimetable:
    stud_name: str
    degree_name: str
    sem: str
    reg_no: str
    center_name: str
    subjects: List[PracticalSubject]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional["PracticalTimetable"]:
        required = ["fname", "fdegree", "fexamname", "fregno", "centrename", "fsubname"]
        if not all(k in data and data[k] for k in required):
            return None

        # Build subjects
        subjects: List[PracticalSubject] = []
        for sub_code, sub_name, exam_date, exam_no, batch, exam_time in zip(
            data.get("fcsubcode", []),
            data.get("fsubname", []),
            data.get("fexamdate", []),
            data.get("fexamno", []),
            data.get("fbatch", []),
            data.get("fexamtime", []),
        ):
            subjects.append(
                PracticalSubject(
                    sub_code=sub_code,
                    sub_name=sub_name,
                    exam_date=exam_date,
                    exam_no=exam_no,
                    batch=batch,
                    exam_time=exam_time,
                )
            )

        return cls(
            stud_name=data.get("fname"),
            degree_name=data.get("fdegree"),
            sem=data.get("fexamname"),
            reg_no=data.get("fregno"),
            center_name=data.get("centrename"),
            subjects=subjects,
        )
