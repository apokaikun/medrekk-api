from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientFamilyHistory
from medrekk.mrs.schemas.patients import (
    PatientFamilyHistoryCreate,
    PatientFamilyHistoryUpdate,
)
from medrekk.common.utils import shortid


def create_family_history(
    patient_id: str,
    family_history: PatientFamilyHistoryCreate,
    db: Session,
) -> PatientFamilyHistory:
    try:
        new_family_history = PatientFamilyHistory(**family_history.model_dump())
        new_family_history.id = shortid()
        new_family_history.patient_id = patient_id

        db.add(new_family_history)
        db.commit()
        db.refresh(new_family_history)

        return new_family_history
    except DBAPIError as e:
        args: str = e.orig.args[0] if e.orig.args else ""
        has_patient_id = args.find("patient_id") >= 0

        if isinstance(e.orig, UniqueViolation) and has_patient_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": "Patient family history already exists.",
                        "loc": "patient_id",
                    },
                },
            )

        raise e


def read_family_history(
    patient_id: str,
    db: Session,
) -> PatientFamilyHistory:
    family_history_db = (
        db.query(PatientFamilyHistory)
        .filter(PatientFamilyHistory.patient_id == patient_id)
        .one_or_none()
    )

    if not family_history_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": "Patient family history data NOT FOUND.",
                    "loc": "patient_id",
                },
            },
        )

    return family_history_db


def update_family_history(
    patient_id: str,
    family_history: PatientFamilyHistoryUpdate,
    db: Session,
) -> PatientFamilyHistory:
    family_history_db = read_family_history(patient_id, db)

    for field, value in family_history.model_dump(exclude_unset=True).items():
        setattr(family_history_db, field, value)

    db.add(family_history_db)
    db.commit()
    db.refresh(family_history_db)

    return family_history_db


def delete_family_history(
    patient_id: str,
    db: Session,
) -> None:
    family_history_db = read_family_history(patient_id, db)

    db.delete(family_history_db)
    db.commit()

    return None
