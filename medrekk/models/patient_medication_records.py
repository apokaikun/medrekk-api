from datetime import date
from typing import Optional
from medrekk.models import MedRekkBase


class MedRekkMedicationRecords(MedRekkBase, table=True):
    __tablename__ = "medrekk_medication_records"

    medication: str
    start_date: Optional[date]
    end_date: Optional[date]
    notes: Optional[str]
