from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientOBHistory
from medrekk.mrs.schemas.patients import PatientOBHistoryCreate, PatientOBHistoryUpdate
from medrekk.common.utils import shortid


def create_ob_history(
    patient_id: str,
    ob_history: PatientOBHistoryCreate,
    db: Session,
) -> PatientOBHistory:
    try:
        new_ob_history = PatientOBHistory(**ob_history.model_dump())
        new_ob_history.id = shortid()
        new_ob_history.patient_id = patient_id

        db.add(new_ob_history)
        db.commit()
        db.refresh(new_ob_history)

        return new_ob_history
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("patient_id") >= 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient ob history already exists."
                        },
                    },
                )


def read_ob_history(
    patient_id: str,
    db: Session,
) -> PatientOBHistory:
    ob_history_db = (
        db.query(PatientOBHistory)
        .filter(PatientOBHistory.patient_id == patient_id)
        .one_or_none()
    )

    if not ob_history_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient ob history data NOT FOUND."},
            },
        )

    return ob_history_db


def update_ob_history(
    patient_id: str,
    ob_history: PatientOBHistoryUpdate,
    db: Session,
) -> PatientOBHistory:
    ob_history_db = read_ob_history(patient_id, db)

    for field, value in ob_history.model_dump(exclude_unset=True).items():
        setattr(ob_history_db, field, value)

    db.add(ob_history_db)
    db.commit()
    db.refresh(ob_history_db)

    return ob_history_db



def delete_ob_history(
    patient_id: str,
    db: Session,
) -> None:
    ob_history_db = read_ob_history(patient_id, db)

    db.delete(ob_history_db)
    db.commit()

    return None

