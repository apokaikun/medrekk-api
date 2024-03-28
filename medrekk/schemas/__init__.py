from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .account_users import (
    AccountCreate,
    AccountRead,
    AccountUpdate,
    ProfileCreate,
    ProfileRead,
    UserBase,
    UserCreate,
    UserRead,
    UserUpdate,
    Users,
    UserListItem,
)

from .patients import (
    PatientProfileCreate,
    PatientProfileRead,
    PatientProfileDelete,
    PatientProfileUpdate,
    PatientBloodPressureCreate,
    PatientBloodPressureRead,
    PatientBloodPressureUpdate,
    PatientBloodPressureDelete,
    PatientHeartRateCreate,
    PatientHeartRateRead,
    PatientHeartRateUpdate,
    PatientHeartRateDelete,
)


class MedRekkBaseSchema(BaseModel):
    id: str
    created: datetime
    updated: datetime

    model_config = ConfigDict(
        from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True
    )


__all__ = [
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserListItem",
    "Users",
    "AccountCreate",
    "AccountRead",
    "AccountUpdate",
    "ProfileCreate",
    "ProfileRead",
    "PatientProfileCreate",
    "PatientProfileRead",
    "PatientProfileDelete",
    "PatientProfileUpdate",
    "PatientBloodPressureCreate",
    "PatientBloodPressureRead",
    "PatientBloodPressureUpdate",
    "PatientBloodPressureDelete",
    "PatientHeartRateCreate",
    "PatientHeartRateRead",
    "PatientHeartRateUpdate",
    "PatientHeartRateDelete",
]
