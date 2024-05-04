from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientHospitalizationHistory
from medrekk.mrs.schemas.patients import (
    PatientHospitalizationHistoryCreate,
    PatientHospitalizationHistoryUpdate,
)
from medrekk.common.utils import shortid


def create_hospitalization_history(
    patient_id: str,
    hospitalization_history: PatientHospitalizationHistoryCreate,
    db: Session,
) -> PatientHospitalizationHistory:
    try:
        new_hospitalization_history = PatientHospitalizationHistory(
            **hospitalization_history.model_dump()
        )
        new_hospitalization_history.id = shortid()
        new_hospitalization_history.patient_id = patient_id

        db.add(new_hospitalization_history)
        db.commit()
        db.refresh(new_hospitalization_history)

        return new_hospitalization_history
    except DBAPIError as e:
        args: str = e.orig.args[0] if e.orig.args else ""
        has_patient_id = args.find("patient_id") >= 0

        if isinstance(e.orig, UniqueViolation) and has_patient_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": "Patient hospitalization history already exists.",
                        "loc": "patient_id",
                    },
                },
            )

        raise e


def read_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    db: Session,
) -> PatientHospitalizationHistory:
    hospitalization_history_db = (
        db.query(PatientHospitalizationHistory)
        .filter(PatientHospitalizationHistory.patient_id == patient_id)
        .filter(PatientHospitalizationHistory.id == hospitalization_history_id)
        .one_or_none()
    )

    if not hospitalization_history_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": "Patient hospitalization history data NOT FOUND.",
                    "loc": "hospitalization_history_id",
                },
            },
        )

    return hospitalization_history_db


def read_hospitalization_histories(
    patient_id: str,
    db: Session,
) -> List[PatientHospitalizationHistory]:
    hospitalization_histories = (
        db.query(PatientHospitalizationHistory)
        .filter(PatientHospitalizationHistory.patient_id == patient_id)
        .order_by(PatientHospitalizationHistory.created.desc())
        .all()
    )

    return hospitalization_histories


def update_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    hospitalization_history: PatientHospitalizationHistoryUpdate,
    db: Session,
) -> PatientHospitalizationHistory:
    hospitalization_history_db = read_hospitalization_history(
        patient_id, hospitalization_history_id, db
    )

    for field, value in hospitalization_history.model_dump(exclude_unset=True).items():
        setattr(hospitalization_history_db, field, value)

    db.add(hospitalization_history_db)
    db.commit()
    db.refresh(hospitalization_history_db)

    return hospitalization_history_db


def delete_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    db: Session,
) -> None:
    hospitalization_history_db = read_hospitalization_history(
        patient_id, hospitalization_history_id, db
    )

    db.delete(hospitalization_history_db)
    db.commit()

    return None
