from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientMedicalHistory
from medrekk.mrs.schemas.patients import (
    PatientMedicalHistoryCreate,
    PatientMedicalHistoryUpdate,
)
from medrekk.common.utils import shortid


def create_medical_history(
    patient_id: str,
    medical_history: PatientMedicalHistoryCreate,
    db: Session,
) -> PatientMedicalHistory:
    try:
        new_medical_history = PatientMedicalHistory(**medical_history.model_dump())
        new_medical_history.id = shortid()
        new_medical_history.patient_id = patient_id

        db.add(new_medical_history)
        db.commit()
        db.refresh(new_medical_history)

        return new_medical_history
    except DBAPIError as e:
        args: str = e.orig.args[0] if e.orig.args else ""
        has_patient_id = args.find("patient_id") >= 0

        if isinstance(e.orig, UniqueViolation) and has_patient_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": "Patient medical history already exists.",
                        "loc": "patient_id",
                    },
                },
            )

        raise e


def read_medical_history(
    patient_id: str,
    db: Session,
) -> PatientMedicalHistory:
    medical_history_db = (
        db.query(PatientMedicalHistory)
        .filter(PatientMedicalHistory.patient_id == patient_id)
        .one_or_none()
    )

    if not medical_history_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": "Patient medical history data NOT FOUND.",
                    "loc": "patient_id",
                },
            },
        )

    return medical_history_db


def update_medical_history(
    patient_id: str,
    medical_history: PatientMedicalHistoryUpdate,
    db: Session,
) -> PatientMedicalHistory:
    medical_history_db = read_medical_history(patient_id, db)

    for field, value in medical_history.model_dump(exclude_unset=True).items():
        setattr(medical_history_db, field, value)

    db.add(medical_history_db)
    db.commit()
    db.refresh(medical_history_db)

    return medical_history_db


def delete_medical_history(
    patient_id: str,
    db: Session,
) -> None:
    medical_history_db = read_medical_history(patient_id, db)

    db.delete(medical_history_db)
    db.commit()

    return None
