from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientBodyTemperature
from medrekk.mrs.schemas.patients import (
    PatientBodyTemperatureCreate,
    PatientBodyTemperatureUpdate,
)
from medrekk.common.utils import shortid


def create_bodytemp(
    record_id: str,
    bodytemp: PatientBodyTemperatureCreate,
    db: Session,
) -> PatientBodyTemperature:
    try:
        new_bodytemp = PatientBodyTemperature(**bodytemp.model_dump())
        new_bodytemp.id = shortid()
        new_bodytemp.record_id = record_id

        db.add(new_bodytemp)
        db.commit()
        db.refresh(new_bodytemp)

        return new_bodytemp
    except DBAPIError as e:
        args: str = e.orig.args[0] if e.orig.args else ""
        has_uc_bodytemperature_patient_dt = (
            args.find("uc_bodytemperature_patient_dt") >= 0
        )

        if isinstance(e.orig, UniqueViolation) and has_uc_bodytemperature_patient_dt:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": "Patient cannot have multiple measurements "
                        "for the same date and time. Date/Time: "
                        f"{new_bodytemp.dt_measured}",
                        "loc": "dt_measured",
                    },
                },
            )
        raise e


def read_bodytemps(
    record_id: str,
    db: Session,
) -> List[PatientBodyTemperature]:
    bodytemps = (
        db.query(PatientBodyTemperature)
        .filter(PatientBodyTemperature.record_id == record_id)
        .all()
    )
    return bodytemps


def read_bodytemp(
    record_id: str,
    bodytemp_id: str,
    db: Session,
) -> List[PatientBodyTemperature]:
    bodytemp = (
        db.query(PatientBodyTemperature)
        .filter(PatientBodyTemperature.record_id == record_id)
        .filter(PatientBodyTemperature.id == bodytemp_id)
        .one_or_none()
    )

    if not bodytemp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Body temperature data NOT FOUND.",
                    "loc": "bodytemp_id",
                },
            },
        )
    return bodytemp


def update_bodytemp(
    record_id: str,
    bodytemp_id: str,
    bodytemp: PatientBodyTemperatureUpdate,
    db: Session,
) -> PatientBodyTemperature:
    bodytemp_db = read_bodytemp(record_id, bodytemp_id, db)

    for field, value in bodytemp.model_dump().items():
        setattr(bodytemp_db, field, value)

    db.add(bodytemp_db)
    db.commit()
    db.refresh(bodytemp_db)

    return bodytemp_db


def delete_bodytemp(
    record_id: str,
    bodytemp_id: str,
    db: Session,
) -> None:
    bodytemp_db = read_bodytemp(record_id, bodytemp_id, db)

    db.delete(bodytemp_db)
    db.commit()

    return None
