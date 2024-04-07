from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientProfile
from medrekk.patient.schemas.patients import PatientProfileCreate
from medrekk.common.utils import shortid


def create_patient(
    patient: PatientProfileCreate,
    db: Session,
):
    new_patient = PatientProfile(**patient.model_dump())
    new_patient.id = shortid()
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    if not new_patient:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )

    return new_patient


def read_patients(
    db: Session,
) -> List[PatientProfile]:
    try:
        patients = db.query(PatientProfile).all()

        return patients
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )


def read_patient(
    patient_id: str,
    db: Session,
) -> PatientProfile:
    patient = db.get(PatientProfile, patient_id)

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Patient with ID: {patient_id} is not found. Please",
                },
            },
        )
    return patient


def update_patient(patient_id: str, db: Session):
    pass
