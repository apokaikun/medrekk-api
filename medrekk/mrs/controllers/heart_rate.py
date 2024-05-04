from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientHeartRate
from medrekk.mrs.schemas.patients import PatientHeartRateCreate, PatientHeartRateUpdate
from medrekk.common.utils import shortid


def create_patient_heartrate(
    record_id: str,
    heartrate: PatientHeartRateCreate,
    db: Session,
) -> PatientHeartRate:
    try:
        new_heartrate = PatientHeartRate(**heartrate.model_dump())
        new_heartrate.record_id = record_id
        new_heartrate.id = shortid()

        db.add(new_heartrate)
        db.commit()
        db.refresh(new_heartrate)

        return new_heartrate
    except DBAPIError as e:
        args: str = e.orig.args[0] if e.orig.args else ""
        has_uc_heartrate_patient_dt = args.find("uc_heartrate_patient_dt") >= 0

        if isinstance(e.orig, UniqueViolation) and has_uc_heartrate_patient_dt:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": f"Patient cannot have multiple measurements for the same date and time. Date/Time: {new_heartrate.dt_measured}",
                        "loc": "dt_measured",
                    },
                },
            )
        raise e


def read_patient_heartrate(
    record_id: str,
    heartrate_id: str,
    db: Session,
) -> PatientHeartRate:
    patient_heartrate = (
        db.query(PatientHeartRate)
        .filter(PatientHeartRate.record_id == record_id)
        .filter(PatientHeartRate.id == heartrate_id)
        .one_or_none()
    )

    if not patient_heartrate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Heart rate data NOT FOUND.",
                    "loc": "heartrate_id",
                },
            },
        )

    return patient_heartrate


def read_patient_heartrates(
    record_id: str,
    db: Session,
) -> List[PatientHeartRate]:
    offset = 0
    patient_heartrates = (
        db.query(PatientHeartRate)
        .filter(PatientHeartRate.record_id == record_id)
        .offset(offset)
        .limit(10)
        .all()
    )

    return patient_heartrates


def update_patient_heartrate(
    record_id: str,
    heartrate_id: str,
    heartrate: PatientHeartRateUpdate,
    db: Session,
) -> PatientHeartRate:
    patient_heartrate = read_patient_heartrate(record_id, heartrate_id, db)

    for field, value in heartrate.model_dump(exclude_unset=True).items():
        setattr(patient_heartrate, field, value)

    db.add(patient_heartrate)
    db.commit()
    db.refresh(patient_heartrate)

    return patient_heartrate


def delete_patient_heartrate(
    record_id: str,
    heartrate_id: str,
    db: Session,
) -> None:
    patient_heartrate = read_patient_heartrate(record_id, heartrate_id, db)

    db.delete(patient_heartrate)
    db.commit()

    return None
