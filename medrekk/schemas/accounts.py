from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class MedRekkBaseSchema(BaseModel):
    id: str
    created: datetime
    updated: datetime

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )


# MedRekk Member Schemas
class MemberBase(BaseModel):
    """
    usernames are required to be emails for easy verification.
    """

    username: EmailStr = Field(description="Must be email.")


class MemberCreate(MemberBase):
    password: SecretStr


class MemberRead(MemberBase, MedRekkBaseSchema):
    account_id: str
    active: bool


class MemberUpdate(MemberCreate, MemberRead):
    updated: datetime


class MemberListItem(MemberBase, MedRekkBaseSchema):
    pass


class Members(BaseModel):
    users: List["MemberListItem"]


# MedRekk Account Schemas
class AccountMembersRead(MemberBase, MedRekkBaseSchema):
    active: bool


class AccountCreate(BaseModel):
    account_name: str
    user_name: EmailStr
    password: SecretStr


class AccountUpdate(BaseModel):
    status: Optional[int]
    updated: datetime


class AccountRead(MedRekkBaseSchema):
    account_name: str
    account_subdomain: str    
    owner_id: str
    status: int
    trial_ends_at: datetime


class AccountMembership(AccountCreate, MedRekkBaseSchema):
    owner_id: str
    status: int
    trial_ends_at: datetime


# MedRekk Member Profile Schemas


class ProfileBase(BaseModel):
    pass


class ProfileMemberRead(AccountMembersRead):
    pass


class ProfileCreate(BaseModel):
    lastname: str
    middlename: str
    firstname: str
    suffix: Optional[str]
    birthdate: datetime
    gender: str
    mobile: str
    address_country: str
    address_province: str
    address_city: str
    address_barangay: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    religion: Optional[str]


class ProfileUpdate(ProfileCreate):
    pass


class ProfileRead(MedRekkBaseSchema, ProfileCreate):
    user: "ProfileMemberRead"


class MemberProfileRead(MedRekkBaseSchema, ProfileCreate):
    user_id: str
    pass
