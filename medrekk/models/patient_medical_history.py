from typing import Annotated
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects import postgresql
from sqlmodel import Field
from medrekk.models import MedRekkBase


class MedRekkMedicalHistory(MedRekkBase, table=True):
    __tablename__ = "medrekk_medical_history"

    hypertension: Annotated[bool, Field(
        default=False, sa_column=Column('hypertension', Boolean()))]
    t2dm: Annotated[bool, Field(
        default=False, sa_column=Column('t2dm', Boolean()))]
    asthma: Annotated[bool, Field(
        default=False, sa_column=Column('asthma', Boolean()))]
    cancer: Annotated[bool, Field(
        default=False, sa_column=Column('cancer', Boolean()))]
    others: Annotated[list, Field(
        default=[], sa_column=Column('others', postgresql.ARRAY(String())))]
