from datetime import datetime
from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientSurgicalHistory
from medrekk.patient.schemas.patients import PatientSurgicalHistoryCreate, PatientSurgicalHistoryUpdate
from medrekk.common.utils import shortid


def create_surgical_history(
    patient_id: str,
    surgical_history: PatientSurgicalHistoryCreate,
    db: Session,
) -> PatientSurgicalHistory:
    try:
        new_surgical_history = PatientSurgicalHistory(**surgical_history.model_dump())
        new_surgical_history.id = shortid()
        new_surgical_history.patient_id = patient_id

        db.add(new_surgical_history)
        db.commit()
        db.refresh(new_surgical_history)

        return new_surgical_history
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("patient_id") >= 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient surgical history already exists."
                        },
                    },
                )


def read_surgical_history(
    patient_id: str,
    surgical_history_id: str,
    db: Session,
) -> PatientSurgicalHistory:
    surgical_history_db = (
        db.query(PatientSurgicalHistory)
        .filter(PatientSurgicalHistory.patient_id == patient_id)
        .filter(PatientSurgicalHistory.id == surgical_history_id)
        .one_or_none()
    )

    if not surgical_history_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient surgical history data NOT FOUND."},
            },
        )

    return surgical_history_db


def read_surgical_histories(
    patient_id: str,
    db: Session,
) -> List[PatientSurgicalHistory]:
    surgical_histories = (
        db.query(PatientSurgicalHistory)
        .filter(PatientSurgicalHistory.patient_id == patient_id)
        .order_by(PatientSurgicalHistory.created.desc())
        .all()
    )

    return surgical_histories


def update_surgical_history(
    patient_id: str,
    surgical_history_id: str,
    surgical_history: PatientSurgicalHistoryUpdate,
    db: Session,
) -> PatientSurgicalHistory:
    surgical_history_db = read_surgical_history(patient_id, surgical_history_id, db)

    for field, value in surgical_history.model_dump(exclude_unset=True).items():
        setattr(surgical_history_db, field, value)

    surgical_history_db.updated = datetime.now()
    
    db.add(surgical_history_db)
    db.commit()
    db.refresh(surgical_history_db)

    return surgical_history_db



def delete_surgical_history(
    patient_id: str,
    surgical_history_id: str,
    db: Session,
) -> None:
    surgical_history_db = read_surgical_history(patient_id, surgical_history_id, db)

    db.delete(surgical_history_db)
    db.commit()

    return None

