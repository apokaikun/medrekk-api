
from typing import Annotated
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field
from medrekk.models import MedRekkBase


class MedRekkVitalsBloodPressure(MedRekkBase, table=True):
    __tablename__ = "medrekk_vitals_blood_pressure"

    patient_id: str = Field(
        default=None,
        foreign_key='medrekk_patient_profile.id')
    systolic: float
    diastolic: float


class MedRekkVitalsHeartRate(MedRekkBase, table=True):
    __tablename__ = "medrekk_vitals_heart_rate"

    heart_rate: Annotated[int, Field(
        default=0, sa_column=Column('heart_rate', postgresql.SMALLINT()))]


class MedRekkVitalsRespiratoryRate(MedRekkBase, table=True):
    __tablename__ = "medrekk_vitals_respiratory_rate"

    respiratory_rate: Annotated[int, Field(
        default=0, sa_column=Column('respiratory_rate', postgresql.SMALLINT()))]


class MedRekkVitalsBodyTemperature(MedRekkBase, table=True):
    __tablename__ = "medrekk_vitals_body_temperature"

    body_temperature: Annotated[float, Field(
        default=0, sa_column=Column('body_temperature', postgresql.FLOAT()))]
