from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class PatientBase(BaseModel):
    id: str
    created: datetime
    updated: datetime

# Patient profile
class PatientProfileCreate(PatientBase):
    lastname: str
    middlename: Optional[str] = ''
    firstname: str
    suffix: Optional[str] = ''
    birthdate: date 
    gender: str
    mobile: Optional[str] = None
    address_country: str = "Philippines"
    address_province: str
    address_city: str
    address_barangay: str
    address_line1: str
    address_line2: Optional[str] = ''
    religion: str = "Roman Catholic"

class PatientProfileRead(PatientProfileCreate):
    pass

class PatientProfileUpdate(PatientProfileCreate):
    updated: datetime = datetime.now()

class PatientProfileDelete(BaseModel):
    id: str

