from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientRespiratoryRate
from medrekk.mrs.schemas.patients import (
    PatientRespiratoryRateCreate,
    PatientRespiratoryRateUpdate,
)
from medrekk.common.utils import shortid


def create_respiratory(
    record_id: str,
    respiratory: PatientRespiratoryRateCreate,
    db: Session,
) -> PatientRespiratoryRate:
    try:
        new_respiratory = PatientRespiratoryRate(**respiratory.model_dump())
        new_respiratory.id = shortid()
        new_respiratory.record_id = record_id

        db.add(new_respiratory)
        db.commit()
        db.refresh(new_respiratory)

        return new_respiratory
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("uc_respiratoryrate_patient_dt"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient cannot have multiple measurements "
                            "for the same date and time. Date/Time: "
                            f"{new_respiratory.dt_measured}"
                        },
                    },
                )


def read_respiratories(
    record_id: str,
    db: Session,
) -> List[PatientRespiratoryRate]:
    respiratories = (
        db.query(PatientRespiratoryRate)
        .filter(PatientRespiratoryRate.record_id == record_id)
        .all()
    )
    return respiratories


def read_respiratory(
    record_id: str,
    respiratory_id: str,
    db: Session,
) -> PatientRespiratoryRate:

    respiratory = (
        db.query(PatientRespiratoryRate)
        .filter(PatientRespiratoryRate.record_id == record_id)
        .filter(PatientRespiratoryRate.id == respiratory_id)
        .one_or_none()
    )

    if not respiratory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Respiratory rate data NOT FOUND.",
                },
            },
        )

    return respiratory


def update_respiratory(
    record_id: str,
    respiratory_id: str,
    respiratory: PatientRespiratoryRateUpdate,
    db: Session,
) -> PatientRespiratoryRate:
    respiratory_db = read_respiratory(record_id, respiratory_id, db)

    for field, value in respiratory.model_dump(exclude_unset=True).items():
        setattr(respiratory_db, field, value)

    db.add(respiratory_db)
    db.commit()
    db.refresh(respiratory_db)

    return respiratory_db


def delete_respiratory(
    record_id: str,
    respiratory_id: str,
    db: Session,
) -> None:
    respiratory_db = read_respiratory(record_id, respiratory_id, db)

    db.delete(respiratory_db)
    db.commit()

    return None
