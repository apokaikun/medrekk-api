from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr
from .base import MedRekkBaseModel


class UserBase(BaseModel):
    """
    usernames are required to be emails for easy verification.
    """
    username: EmailStr


class UserCreate(UserBase):
    password: SecretStr


class UserUpdate(UserCreate):
    """
    Pydantic model for updating user's password.
    """
    updated: datetime


class User(UserCreate, MedRekkBaseModel):
    """
    Pydantic model for Users.
    Returns `username` and `id`
    """
    model_config = ConfigDict(from_attributes=True)
