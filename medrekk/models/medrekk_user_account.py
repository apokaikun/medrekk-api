
from datetime import datetime, timedelta
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel
from pydantic import ConfigDict, EmailStr, SecretStr
from sqlalchemy import Boolean, Column, String
from shortuuid import uuid


class MedRekkBase(SQLModel):
    id: str = Field(
        default=uuid(), primary_key=True, unique=True)
    created: datetime = Field(
        nullable=False, default=datetime.now())
    updated: datetime = Field(
        nullable=False, default=datetime.now())


class MedRekkAccountCreate(SQLModel):
    __tablename__ = "medrekk_accounts"

    accountName: str
    ownerID: str = Field(default=None, foreign_key='medrekk_users.id')
    users: List['MedRekkUser'] = Relationship(
        back_populates='accounts')
    status: int = Field(default=1)
    trialEndsAt: datetime = Field(default=datetime.now() + timedelta(days=14))


class MedRekkAccountRead(MedRekkAccountCreate):
    pass


class MedRekkAccount(MedRekkAccountCreate, MedRekkBase, table=True):
    model_config = ConfigDict(from_attributes=True)


class MedRekkUserBase(SQLModel):
    """
    usernames are required to be emails for easy verification.
    """
    username: EmailStr = Field(
        default=None,
        sa_column=Column('username', String()))


class MedRekkUserCreate(MedRekkUserBase):
    password: SecretStr = Field(
        default=None,
        sa_column=Column('password', String()))


class MedRekkUserRead(MedRekkUserBase, MedRekkBase):
    active: bool
    accounts: Optional[List["MedRekkAccount"]]


class MedRekkUserUpdate(MedRekkUserCreate):
    """
    Pydantic model for updating user's password.
    """
    active: bool
    accounts: Optional[List["MedRekkAccount"]]
    updated: datetime


class MedRekkUser(MedRekkUserCreate, MedRekkBase, table=True):
    __tablename__ = "medrekk_users"
    active: bool = Field(
        default=True,
        sa_column=Column('active', Boolean()))
    accounts: Optional[List["MedRekkAccount"]
                       ] = Relationship(back_populates='users')
    model_config = ConfigDict(from_attributes=True)
