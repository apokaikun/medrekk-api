from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientBodyWeight
from medrekk.patient.schemas.patients import (
    PatientBodyWeightCreate,
    PatientBodyWeightUpdate,
)
from medrekk.common.utils import shortid


def create_bodyweight(
    patient_id: str,
    bodyweight: PatientBodyWeightCreate,
    db: Session,
) -> PatientBodyWeight:
    try:
        new_weight = PatientBodyWeight(**bodyweight.model_dump())
        new_weight.id = shortid()
        new_weight.patient_id = patient_id

        db.add(new_weight)
        db.commit()
        db.refresh(new_weight)

        return new_weight
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("uc_bodyweight_patient_date"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient cannot have multiple measurements "
                            "for the same date and time. Date: "
                            f"{new_weight.date_measured}"
                        },
                    },
                )


def read_bodyweight(
    patient_id: str,
    bodyweight_id: str,
    db: Session,
) -> PatientBodyWeight:
    bodyweight = (
        db.query(PatientBodyWeight)
        .filter(PatientBodyWeight.patient_id == patient_id)
        .filter(PatientBodyWeight.id == bodyweight_id)
        .one_or_none()
    )

    if not bodyweight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Body weight data NOT FOUND.",
                },
            },
        )

    return bodyweight


def read_bodyweights(
    patient_id: str,
    db: Session,
) -> List[PatientBodyWeight]:
    bodyweights = (
        db.query(PatientBodyWeight)
        .filter(PatientBodyWeight.patient_id == patient_id)
        .all()
    )

    return bodyweights

def update_bodyweight(
        patient_id: str,
        bodyweight_id: str,
        bodyweight: PatientBodyWeightUpdate,
        db: Session,
) -> PatientBodyWeight:
    bodyweight_db = read_bodyweight(patient_id, bodyweight_id, db)

    for field, value in bodyweight.model_dump().items():
        setattr(bodyweight_db, field, value)

    db.add(bodyweight_db)
    db.commit()
    db.refresh(bodyweight_db)

    return bodyweight_db

def delete_bodyweight(
        patient_id: str,
        bodyweight_id: str,
        db: Session,
) -> None:
    bodyweight_db = read_bodyweight(patient_id, bodyweight_id, db)

    db.delete(bodyweight_db)
    db.commit()

    return None