from datetime import datetime, date
from typing import Optional
from medrekk.models import MedRekkBase


class MedRekkHospitalizationHistory(MedRekkBase, table=True):
    __tablename__ = "medrekk_hospitalization_history"

    chiefcomplaint: str
    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]
