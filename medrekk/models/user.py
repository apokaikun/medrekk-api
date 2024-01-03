
from .base import MedRekkBase
from sqlmodel import Field
from pydantic import EmailStr
from sqlalchemy import Column, String


class MedRekkUser(MedRekkBase, table=True):
    __tablename__ = "medrekk_users"

    username: EmailStr = Field(
        default=None, sa_column=Column('username', String()))
    password: str = Field(default=None, sa_column=Column('password', String()))
