from typing import Optional

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
