from datetime import date
from typing import Annotated, Optional
from sqlalchemy import Column
from sqlmodel import Field
from medrekk.models import MedRekkBase
from sqlalchemy.dialects import postgresql


class MedRekkOBHistory(MedRekkBase, table=True):
    __tablename__ = "medrekk_ob_history"

    gravida: Annotated[int, Field(
        default=0, sa_column=Column("gravida", postgresql.SMALLINT()))]
    para: Annotated[int, Field(
        default=0, sa_column=Column("para", postgresql.SMALLINT()))]
    term: Annotated[int, Field(
        default=0, sa_column=Column("term", postgresql.SMALLINT()))]
    abortion: Annotated[int, Field(
        default=0, sa_column=Column("abortion", postgresql.SMALLINT()))]
    living: Annotated[int, Field(
        default=0, sa_column=Column("living", postgresql.SMALLINT()))]
    lmp: Optional[date]
    others: Optional[str]
    notes: Optional[str]
