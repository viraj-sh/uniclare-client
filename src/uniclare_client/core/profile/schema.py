from pydantic import BaseModel, ConfigDict


class Profile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    # Required — the application needs these
    reg_no: str
    full_name: str
    degree: str

    # Optional — nice to have
    fat_name: str | None = None
    mot_name: str | None = None
    degree_code: str | None = None
    college: str | None = None
    college_code: str | None = None
    photo: str | None = None
    category: str | None = None
    fee_type: str | None = None
    mob_no: str | None = None
    email: str | None = None
    parent_mob_no: str | None = None
