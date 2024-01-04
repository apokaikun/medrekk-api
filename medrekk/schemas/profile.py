from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from .base import MedRekkBaseModel


class ProfileCreate(MedRekkBaseModel):
    lastname: str
    middlename: Optional[str]
    firstname: str

    birthdate: datetime
    gender: str

    mobile: str
    email: EmailStr
    address_country: str
    address_province: str
    address_city: str
    address_barangay: str
    address_line1: str
    address_line2: Optional[str]

    religion: str


class ProfileRead(ProfileCreate):
    pass


class ProfileUpdate(ProfileCreate):
    updated: datetime
