from datetime import date
from typing import Optional
from medrekk.models import MedRekkBase


class MedRekkSurgicalHistory(MedRekkBase, table=True):
    __tablename__ = "medrekk_surgical_history"

    chief_complaint: str
    surgery_date: date
    notes: Optional[str]
