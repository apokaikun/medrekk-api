from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientImmunization
from medrekk.mrs.schemas.patients import (
    PatientImmunizationCreate,
    PatientImmunizationUpdate,
)
from medrekk.common.utils import shortid


def create_immunization(
    patient_id: str,
    immunization: PatientImmunizationCreate,
    db: Session,
) -> PatientImmunization:
    try:
        new_immunization = PatientImmunization(**immunization.model_dump())
        new_immunization.id = shortid()
        new_immunization.patient_id = patient_id

        db.add(new_immunization)
        db.commit()
        db.refresh(new_immunization)

        return new_immunization
    except DBAPIError as e:
        args: str = e.orig.args[0] if e.orig.args else ""
        has_patient_id = args.find("patient_id") >= 0

        if isinstance(e.orig, UniqueViolation) and has_patient_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": "Patient immunization history already exists.",
                        "loc": "patient_id",
                    },
                },
            )

        raise e


def read_immunization(
    patient_id: str,
    immunization_id: str,
    db: Session,
) -> PatientImmunization:
    immunization_db = (
        db.query(PatientImmunization)
        .filter(PatientImmunization.patient_id == patient_id)
        .filter(PatientImmunization.id == immunization_id)
        .one_or_none()
    )

    if not immunization_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient immunization history data NOT FOUND."},
            },
        )

    return immunization_db


def read_immunizations(
    patient_id: str,
    db: Session,
) -> List[PatientImmunization]:
    immunizations = (
        db.query(PatientImmunization)
        .filter(PatientImmunization.patient_id == patient_id)
        .order_by(PatientImmunization.created.desc())
        .all()
    )

    return immunizations


def update_immunization(
    patient_id: str,
    immunization_id: str,
    immunization: PatientImmunizationUpdate,
    db: Session,
) -> PatientImmunization:
    immunization_db = read_immunization(patient_id, immunization_id, db)

    for field, value in immunization.model_dump(exclude_unset=True).items():
        setattr(immunization_db, field, value)

    db.add(immunization_db)
    db.commit()
    db.refresh(immunization_db)

    return immunization_db


def delete_immunization(
    patient_id: str,
    immunization_id: str,
    db: Session,
) -> None:
    immunization_db = read_immunization(patient_id, immunization_id, db)

    db.delete(immunization_db)
    db.commit()

    return None
