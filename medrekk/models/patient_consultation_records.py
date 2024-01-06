from typing import Optional
from sqlmodel import Field, String
from .base import MedRekkBase
from shortuuid import uuid


class MedRekkConsultationRecord(MedRekkBase, table=True):
    __tablename__ = "medrekk_consultation_records"

    chiefComplaint: str
    history: Optional[str]
    notes: Optional[str]
    management: Optional[str]
