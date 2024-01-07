from typing import Annotated

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlmodel import Field
from medrekk.models import MedRekkBase


class MedRekkBiometricsBodyWeight(MedRekkBase, table=True):
    __tablename__ = "medrekk_biometrics_body_weight"

    body_weight: Annotated[float, Field(
        default=0, sa_column=Column('body_weight', postgresql.FLOAT()))]


class MedRekkBiometricsHeight(MedRekkBase, table=True):
    __tablename__ = "medrekk_biometrics_height"

    height: Annotated[float, Field(
        default=0, sa_column=Column('height', postgresql.FLOAT()))]


class MedRekkBiometricsBodyMassIndex(MedRekkBase, table=True):
    __tablename__ = "medrekk_biometrics_bmi"

    bmi: Annotated[float, Field(
        default=0, sa_column=Column('bmi', postgresql.FLOAT()))]
    notes: Annotated[str, Field(
        default='normal')]
