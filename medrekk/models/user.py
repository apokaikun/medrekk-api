
from .base import MedRekkBase
from sqlmodel import Field
from pydantic import EmailStr
from sqlalchemy import Boolean, Column, String


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
