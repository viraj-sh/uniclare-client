from pydantic import BaseModel, Field, model_validator
from typing import Optional, Any, Dict


class ProfileRequestModel(BaseModel):
    refetch: bool = Field(False)


class StudentProfileModel(BaseModel):
    full_name: Optional[str] = Field(None)
    fath_name: Optional[str] = Field(None)
    mot_name: Optional[str] = Field(None)
    degree_id: Optional[str] = Field(None)
    coll_id: Optional[str] = Field(None)
    degree_name: Optional[str] = Field(None)
    coll_name: Optional[str] = Field(None)
    photo: Optional[str] = Field(None)
    category: Optional[str] = Field(None)
    degree_grp: Optional[str] = Field(None)
    fee_type: Optional[str] = Field(None)
    reg_no: Optional[str] = Field(None)
    smobile_no: Optional[str] = Field(None)
    semail: Optional[str] = Field(None)
    pmobile_no: Optional[str] = Field(None)
    exam_date: Optional[str] = Field(None)


class StandardResponseModel(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[Any] = Field(None)
    status_code: int = Field(...)


class EditableProfileData(BaseModel):
    reg_no: str = Field(...)
    full_name: str = Field(...)
    fath_name: Optional[str] = Field(None)
    mot_name: Optional[str] = Field(None)
    abc_id: Optional[str] = Field(None)
    sphoto: Optional[str] = Field(None)

    class Config:
        from_attributes = True


class EditableProfileRequest(BaseModel):
    refetch: Optional[bool] = Field(False)


class StandardResponse(BaseModel):
    success: bool = Field(...)
    error: Optional[str] = Field(None)
    data: Optional[Any] = Field(None)
    status_code: int = Field(...)

    class Config:
        arbitrary_types_allowed = True


class ProfileEditRequest(BaseModel):
    father_name: Optional[str] = Field(None, alias="father_name")
    mother_name: Optional[str] = Field(None, alias="mother_name")
    abc_no: Optional[str] = Field(None, alias="abc_no")

    @model_validator(mode="after")
    def validate_at_least_one_field(self):
        if not (self.father_name or self.mother_name or self.abc_no):
            raise ValueError("At least one editable field must be provided")
        return self


class StandardResponseModel2(BaseModel):
    success: bool
    error: Optional[str]
    data: Optional[Dict[str, Any]]
    status_code: int
