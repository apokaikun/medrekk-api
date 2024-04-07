from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientAllergy
from medrekk.patient.schemas.patients import PatientAllergyCreate, PatientAllergyUpdate
from medrekk.common.utils import shortid


def create_allergy(
    patient_id: str,
    allergy: PatientAllergyCreate,
    db: Session,
) -> PatientAllergy:
    try:
        new_allergy = PatientAllergy(**allergy.model_dump())
        new_allergy.id = shortid()
        new_allergy.patient_id = patient_id

        db.add(new_allergy)
        db.commit()
        db.refresh(new_allergy)

        return new_allergy
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("patient_id") >= 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient hospitalization history already exists."
                        },
                    },
                )


def read_allergy(
    patient_id: str,
    allergy_id: str,
    db: Session,
) -> PatientAllergy:
    allergy_db = (
        db.query(PatientAllergy)
        .filter(PatientAllergy.patient_id == patient_id)
        .filter(PatientAllergy.id == allergy_id)
        .one_or_none()
    )

    if not allergy_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient hospitalization history data NOT FOUND."},
            },
        )

    return allergy_db


def read_allergies(
    patient_id: str,
    db: Session,
) -> List[PatientAllergy]:
    medications = (
        db.query(PatientAllergy)
        .filter(PatientAllergy.patient_id == patient_id)
        .order_by(PatientAllergy.created.desc())
        .all()
    )

    return medications


def update_allergy(
    patient_id: str,
    allergy_id: str,
    allergy: PatientAllergyUpdate,
    db: Session,
) -> PatientAllergy:
    allergy_db = read_allergy(patient_id, allergy_id, db)

    for field, value in allergy.model_dump(exclude_unset=True).items():
        setattr(allergy_db, field, value)

    db.add(allergy_db)
    db.commit()
    db.refresh(allergy_db)

    return allergy_db


def delete_allergy(
    patient_id: str,
    allergy_id: str,
    db: Session,
) -> None:
    allergy_db = read_allergy(patient_id, allergy_id, db)

    db.delete(allergy_db)
    db.commit()

    return None
