from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, SecretStr

from medrekk.schemas.base import MedRekkBaseSchema


# MedRekk User Schemas
class UserBase(BaseModel):
    """
    usernames are required to be emails for easy verification.
    """

    username: EmailStr = Field(description="Must be email.")


class UserCreate(UserBase):
    password: SecretStr


class UserRead(UserBase, MedRekkBaseSchema):
    active: bool
    memberships: List["AccountMembership"]
    profile: Optional["UserProfileRead"]

class UserUpdate(UserCreate, UserRead):
    updated: datetime

class UserListItem(UserBase, MedRekkBaseSchema):
    pass

class Users(BaseModel):
    users: List["UserListItem"]

# MedRekk Account Schemas
class AccountMembersRead(UserBase, MedRekkBaseSchema):
    active: bool


class AccountCreate(BaseModel):
    account_name: str


class AccountUpdate(BaseModel):
    status: Optional[int]
    updated: datetime


class AccountRead(AccountCreate, MedRekkBaseSchema):
    owner_id: str
    status: int
    trial_ends_at: datetime
    owner: "AccountMembersRead"
    members: List["AccountMembersRead"]


class AccountMembership(AccountCreate, MedRekkBaseSchema):
    owner_id: str
    status: int
    trial_ends_at: datetime


# MedRekk User Profile Schemas


class ProfileBase(BaseModel):
    pass


class ProfileUserRead(AccountMembersRead):
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
    user: "ProfileUserRead"


class UserProfileRead(MedRekkBaseSchema, ProfileCreate):
    user_id: str
    pass
