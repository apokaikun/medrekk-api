from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    """
    Pydantic model for updating user's password.
    """

    updated: datetime


class User(UserBase):
    """
    Pydantic model for Users.
    Returns `email` and `id`
    """
    id: str

    model_config = ConfigDict(from_attributes=True)
