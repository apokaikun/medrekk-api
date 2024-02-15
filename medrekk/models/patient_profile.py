from datetime import datetime
from typing import Optional

from shortuuid import uuid
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from sqlalchemy import Column, String


class MedRekkPatientBase(SQLModel):
    id: str = Field(
        default=uuid(), primary_key=True, unique=True)
    created: datetime = Field(
        nullable=False, default=datetime.now())
    updated: datetime = Field(
        nullable=False, default=datetime.now())


class MedRekkPatientProfile(MedRekkPatientBase, table=True):
    __tablename__ = "medrekk_patient_profile"

    lastname: str = Field(nullable=False)
    middlename: Optional[str]
    firstname: str = Field(nullable=False)
    suffix: Optional[str]
    birthdate: datetime
    gender: str
    mobile: str
    email: EmailStr = Field(sa_column=Column(String()))
    address_country: str
    address_province: str
    address_city: str
    address_barangay: str
    address_line1: str
    address_line2: Optional[str]
    religion: str
