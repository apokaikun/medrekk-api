from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientBloodPressure
from medrekk.mrs.schemas.patients import (
    PatientBloodPressureCreate,
    PatientBloodPressureUpdate,
)
from medrekk.common.utils import shortid


def create_patient_bloodpressure(
    record_id: str,
    patient_bp: PatientBloodPressureCreate,
    db: Session,
) -> PatientBloodPressure:
    try:
        new_bp = PatientBloodPressure(**patient_bp.model_dump())
        new_bp.record_id = record_id
        new_bp.id = shortid()
        db.add(new_bp)
        db.commit()
        db.refresh(new_bp)

        return new_bp
    except DBAPIError as e:
        arg: str = e.orig.args[0] if e.orig.args else ""
        has_uc_bloodpressure_patient_dt = arg.find("uc_bloodpressure_patient_dt") >= 0

        if isinstance(e.orig, UniqueViolation) and has_uc_bloodpressure_patient_dt:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": f"Patient cannot have multiple measurements for the same date and time. Date/Time: {new_bp.dt_measured}",
                        "loc": "dt_measured",
                    },
                },
            )
        raise e


def read_patient_bloodpressure(
    record_id: str,
    bp_id: str,
    db: Session,
) -> PatientBloodPressure:
    patient_bp = (
        db.query(PatientBloodPressure)
        .filter(PatientBloodPressure.record_id == record_id)
        .filter(PatientBloodPressure.id == bp_id)
        .one_or_none()
    )

    if not patient_bp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Blood pressure data NOT FOUND.",
                    "loc": "bp_id",
                },
            },
        )
    return patient_bp


def read_patient_bloodpressures(
    record_id: str,
    db: Session,
) -> List[PatientBloodPressure]:
    patient_bps = (
        db.query(PatientBloodPressure)
        .filter(PatientBloodPressure.record_id == record_id)
        .order_by(PatientBloodPressure.created.desc())
        .all()
    )
    return patient_bps


def update_patient_bloodpressure(
    record_id: str,
    bp_id: str,
    bp: PatientBloodPressureUpdate,
    db: Session,
) -> PatientBloodPressure:
    patient_bp = read_patient_bloodpressure(record_id, bp_id, db)

    for field, value in bp.model_dump(exclude_unset=True).items():
        setattr(patient_bp, field, value)

    db.add(patient_bp)
    db.commit()
    db.refresh(patient_bp)

    return patient_bp


def delete_patient_bloodpressure(
    record_id: str,
    bp_id: str,
    db: Session,
) -> None:
    patient_bp = read_patient_bloodpressure(record_id, bp_id, db)

    db.delete(patient_bp)
    db.commit()

    return None
