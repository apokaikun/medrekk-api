from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientMedication
from medrekk.mrs.schemas.patients import PatientMedicationCreate, PatientMedicationUpdate
from medrekk.common.utils import shortid


def create_medication(
    patient_id: str,
    medication: PatientMedicationCreate,
    db: Session,
) -> PatientMedication:
    try:
        new_medication = PatientMedication(**medication.model_dump())
        new_medication.id = shortid()
        new_medication.patient_id = patient_id

        db.add(new_medication)
        db.commit()
        db.refresh(new_medication)

        return new_medication
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("patient_id") >= 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient medication history already exists."
                        },
                    },
                )


def read_medication(
    patient_id: str,
    medication_id: str,
    db: Session,
) -> PatientMedication:
    medication_db = (
        db.query(PatientMedication)
        .filter(PatientMedication.patient_id == patient_id)
        .filter(PatientMedication.id == medication_id)
        .one_or_none()
    )

    if not medication_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient medication history data NOT FOUND."},
            },
        )

    return medication_db


def read_medications(
    patient_id: str,
    db: Session,
) -> List[PatientMedication]:
    medications = (
        db.query(PatientMedication)
        .filter(PatientMedication.patient_id == patient_id)
        .order_by(PatientMedication.created.desc())
        .all()
    )

    return medications


def update_medication(
    patient_id: str,
    medication_id: str,
    medication: PatientMedicationUpdate,
    db: Session,
) -> PatientMedication:
    medication_db = read_medication(patient_id, medication_id, db)

    for field, value in medication.model_dump(exclude_unset=True).items():
        setattr(medication_db, field, value)

    db.add(medication_db)
    db.commit()
    db.refresh(medication_db)

    return medication_db



def delete_medication(
    patient_id: str,
    medication_id: str,
    db: Session,
) -> None:
    medication_db = read_medication(patient_id, medication_id, db)

    db.delete(medication_db)
    db.commit()

    return None

