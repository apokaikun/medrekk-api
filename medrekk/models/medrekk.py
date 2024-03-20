from datetime import datetime, timedelta
from typing import List

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey,
                        SmallInteger, String, Table)
from sqlalchemy.orm import Mapped, relationship

from medrekk.database.connection import Base
from medrekk.utils import shortid


class MedRekkBase:
    id = Column(String, default=shortid(), primary_key=True)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())


medrekk_account_user_assoc = Table(
    "medrekk_account_users_assoc",
    Base.metadata,
    Column("user_id", ForeignKey("medrekk_users.id"), primary_key=True),
    Column("account_id", ForeignKey("medrekk_accounts.id"), primary_key=True),
)


class MedRekkUser(Base, MedRekkBase):
    __tablename__ = "medrekk_users"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active: bool = Column(
        Boolean,
        default=True,
    )

    # Relationships
    profile = relationship("MedRekkUserProfile", back_populates="user", uselist=False)
    memberships: Mapped[List["MedRekkAccount"]] = relationship(
        "MedRekkAccount", secondary=medrekk_account_user_assoc
    )


class MedRekkAccount(Base, MedRekkBase):
    __tablename__ = "medrekk_accounts"

    account_name = Column(String, nullable=False)
    owner_id = Column(ForeignKey("medrekk_users.id"))
    status = Column(SmallInteger, default=1)
    trial_ends_at = Column(DateTime, default=datetime.now() + timedelta(days=14))

    # Relationships
    owner = relationship("MedRekkUser", uselist=False)
    members: Mapped[List["MedRekkUser"]] = relationship(
        "MedRekkUser", secondary=medrekk_account_user_assoc
    )


class MedRekkUserProfile(Base, MedRekkBase):
    __tablename__ = "medrekk_user_profiles"

    user_id = Column(String, ForeignKey("medrekk_users.id"), unique=True)
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

    # Relationships
    user = relationship("MedRekkUser", back_populates="profile", uselist=False)
