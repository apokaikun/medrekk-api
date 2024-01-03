from sqlmodel import Field, String
from .base import MedRekkBase
from shortuuid import uuid


class MedRekkPatientConsultationRecord(MedRekkBase, table=True):
    __tablename__ = "medrekk_patient_consultation_records"

    chiefComplaint: str
    history: str
    notes: str
    management: str
