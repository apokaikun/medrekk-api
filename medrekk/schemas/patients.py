from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class PatientBase(BaseModel):
    id: str
    created: datetime
    updated: datetime

    model_config = ConfigDict(
        from_attributes = True,
        validate_assignment = True,
        arbitrary_types_allowed = True
        )

# Patient profile
class PatientProfileCreate(BaseModel):
    lastname: str = Field(title="Patient Lastname")
    middlename: Optional[str] = ''
    firstname: str
    suffix: Optional[str] = ''
    birthdate: date 
    gender: str
    mobile: Optional[str] = None
    email: Optional[str] = None
    address_country: str = "Philippines"
    address_province: str
    address_city: str
    address_barangay: str
    address_line1: str
    address_line2: Optional[str] = ''
    religion: str = "Roman Catholic"
    
    # model_config = PatientBase.model_config
    # model_config["title"] = "Patient Profile Create"

class PatientProfileRead(PatientProfileCreate, PatientBase):
    url: str = ''
    pass

class PatientProfileUpdate(PatientProfileCreate):
    updated: datetime = datetime.now()

class PatientProfileDelete(BaseModel):
    id: str

