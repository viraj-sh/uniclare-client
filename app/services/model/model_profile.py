from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class StudentProfile:
    full_name: Optional[str]
    fath_name: Optional[str]
    mot_name: Optional[str]
    degree_id: Optional[str]
    coll_id: Optional[str]
    degree_name: Optional[str]
    coll_name: Optional[str]
    photo: Optional[str]
    category: Optional[str]
    degree_grp: Optional[str]
    fee_type: Optional[str]
    reg_no: Optional[str]
    smobile_no: Optional[str]
    semail: Optional[str]
    pmobile_no: Optional[str]
    exam_date: Optional[str]

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional["StudentProfile"]:
        if not isinstance(data, dict):
            return None
        if data.get("status") != "success":
            return None

        return cls(
            full_name=data.get("fname"),
            fath_name=data.get("ffatname"),
            mot_name=data.get("fmotname"),
            degree_id=data.get("fdegree"),
            coll_id=data.get("fcollcode"),
            degree_name=data.get("degree"),
            coll_name=data.get("college"),
            photo=data.get("photopath"),
            category=data.get("category"),
            degree_grp=data.get("fdeggrp"),
            fee_type=data.get("feetype"),
            reg_no=data.get("strRegno"),
            smobile_no=data.get("strMobile"),
            semail=data.get("strEmail"),
            pmobile_no=data.get("strParentMob"),
            exam_date=data.get("strExamdate"),
        )


@dataclass
class EditableProfile:
    reg_no: str
    full_name: str
    fath_name: Optional[str] = None
    abc_id: Optional[str] = None
    mot_name: Optional[str] = None
    sphoto: Optional[str] = None

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional["EditableProfile"]:
        if not isinstance(data, dict):
            return None

        try:
            studdet = data["data"]["studdet"]
            return cls(
                reg_no=studdet["fregno"],
                full_name=studdet["fname"],
                fath_name=studdet.get("ffatname"),
                abc_id=studdet.get("fabcno"),
                mot_name=studdet.get("fmotname"),
                sphoto=studdet.get("fphotopath"),
            )
        except (KeyError, TypeError):
            return None
