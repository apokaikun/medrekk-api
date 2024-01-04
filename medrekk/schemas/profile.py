from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class ProfileBase(BaseModel):
    lastname: str
    middlename: Optional[str]
    firstname: str

    birthdate: datetime
    gender: str

    mobile: str
    address_country: str
    address_province: str
    address_city: str
    address_barangay: str
    address_line1: str
    address_line2: Optional[str]

    religion: str


class ProfileCreate(ProfileBase):
    user_id: str


class ProfileUpdate(ProfileBase):
    updated: datetime


class Profile(ProfileBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
