from datetime import datetime, timedelta
from typing import List
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, relationship

from medrekk.common.database.connection import Base
from medrekk.common.utils import shortid


class MedRekkBase:
    id = Column(String, default=shortid(), primary_key=True)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

medrekk_account_user_assoc = Table(
    "medrekk_account_member_assoc",
    Base.metadata,
    Column("member_id", ForeignKey("medrekk_members.id"), primary_key=True),
    Column("account_id", ForeignKey("medrekk_accounts.id"), primary_key=True),
)

class MedRekkMember(Base, MedRekkBase):
    __tablename__ = "medrekk_members"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active: bool = Column(Boolean, default=True)
    account_id = Column(ForeignKey("medrekk_accounts.id", name="member_account"))

class MedRekkAccount(Base, MedRekkBase):
    __tablename__ = "medrekk_accounts"

    account_name = Column(String, nullable=False)
    account_subdomain = Column(String, nullable=False)
    owner_id = Column(ForeignKey("medrekk_members.id", name="account_owner"))
    status = Column(SmallInteger, default=1)
    trial_ends_at = Column(DateTime, default=datetime.now() + timedelta(days=14))

    members: Mapped[List["MedRekkMember"]] = relationship("MedRekkMember", secondary=medrekk_account_user_assoc)


class MedRekkMemberProfile(Base, MedRekkBase):
    __tablename__ = "medrekk_member_profiles"

    member_id = Column(String, ForeignKey("medrekk_members.id"), unique=True)
    lastname = Column(String, nullable=False)
    middlename = Column(String, nullable=True)
    firstname = Column(String, nullable=False)
    suffix = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    address_country = Column(String, nullable=False)
    address_province = Column(String, nullable=False)
    address_city = Column(String, nullable=False)
    address_barangay = Column(String, nullable=False)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)
    religion = Column(String, nullable=False)
