from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql
from sqlmodel import Field
from medrekk.models.base import MedRekkBase
from shortuuid import uuid


def getTrialEndsAt() -> datetime:
    return datetime.now() + timedelta(days=14)


class MedRekkAccount(MedRekkBase, table=True):
    __tablename__ = "medrekk_accounts"

    ownerID: str = Field(
        default=uuid(), primary_key=True, unique=True)
    accountName: str
    members: Optional[List[str]] = Field(
        default=None,
        sa_column=Column(postgresql.ARRAY(String())))
    status: int = Field(default=1)
    trialEndsAt: datetime = Field(default=getTrialEndsAt())
