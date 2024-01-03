from sqlmodel import Field, SQLModel
from datetime import datetime
from shortuuid import uuid


class MedRekkBase(SQLModel):
    id: str = Field(
        default=uuid(), primary_key=True, unique=True)
    created: datetime = Field(
        nullable=False, default=datetime.now())
    updated: datetime = Field(
        nullable=False, default=datetime.now())
