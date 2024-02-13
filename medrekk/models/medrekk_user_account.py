
from datetime import datetime, timedelta
from typing import List, Optional

from sqlmodel import Field, Relationship
from pydantic import EmailStr
from sqlalchemy import Boolean, Column, String

from medrekk.models.base import MedRekkBase


class MedRekkUser(MedRekkBase, table=True):
    __tablename__ = "medrekk_users"

    active: bool = Field(
        default=True,
        sa_column=Column('active', Boolean()))

    username: EmailStr = Field(
        default=None,
        sa_column=Column('username', String()))
    password: str = Field(
        default=None,
        sa_column=Column('password', String()))
    accounts: Optional[List["MedRekkAccount"]
                       ] = Relationship(back_populates='users')


class MedRekkAccount(MedRekkBase, table=True):
    __tablename__ = "medrekk_accounts"

    accountName: str
    ownerID: str = Field(default=None, foreign_key='medrekk_users.id')
    users: List['MedRekkUser'] = Relationship(
        back_populates='accounts')
    status: int = Field(default=1)
    trialEndsAt: datetime = Field(default=datetime.now() + timedelta(days=14))
