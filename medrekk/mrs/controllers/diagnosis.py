from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientDiagnosis
from medrekk.mrs.schemas.patients import (
    PatientDiagnosisCreate,
    PatientDiagnosisUpdate,
)
from medrekk.common.utils import shortid


def create_patient_diagnosis(
    record_id: str,
    diagnosis: PatientDiagnosisCreate,
    db: Session,
) -> PatientDiagnosis:
    try:
        new_diagnosis = PatientDiagnosis(**diagnosis.model_dump())
        new_diagnosis.record_id = record_id
        new_diagnosis.id = shortid()
        db.add(new_diagnosis)
        db.commit()
        db.refresh(new_diagnosis)

        return new_diagnosis
    except DBAPIError as e:
        args: str = e.orig.args[0] if e.orig.args else ""
        has_uc_record_diagnosis = args.find("uc_record_diagnosis") >= 0

        if isinstance(e.orig, UniqueViolation) and has_uc_record_diagnosis:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": f"Patient cannot have the same diagnosis in one record: {new_diagnosis.diagnosis_code}",
                            "loc": "record_id"
                        },
                    },
                )
        raise e


def read_patient_diagnosis(
    record_id: str,
    diagnosis_id: str,
    db: Session,
) -> PatientDiagnosis:
    diagnosis = (
        db.query(PatientDiagnosis)
        .filter(PatientDiagnosis.record_id == record_id)
        .filter(PatientDiagnosis.id == diagnosis_id)
        .one_or_none()
    )

    if not diagnosis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Diagnosis data NOT FOUND.",
                },
            },
        )
    return diagnosis


def read_patient_diagnoses(
    record_id: str,
    db: Session,
) -> List[PatientDiagnosis]:
    diagnoses = (
        db.query(PatientDiagnosis)
        .filter(PatientDiagnosis.record_id == record_id)
        .order_by(PatientDiagnosis.created.desc())
        .all()
    )
    return diagnoses


def update_patient_diagnosis(
    record_id: str,
    diagnosis_id: str,
    diagnosis: PatientDiagnosisUpdate,
    db: Session,
) -> PatientDiagnosis:
    diagnosis_db = read_patient_diagnosis(record_id, diagnosis_id, db)

    for field, value in diagnosis.model_dump(exclude_unset=True).items():
        setattr(diagnosis_db, field, value)

    db.add(diagnosis_db)
    db.commit()
    db.refresh(diagnosis_db)

    return diagnosis_db


def delete_patient_diagnosis(
    record_id: str,
    diagnosis_id: str,
    db: Session,
) -> None:
    diagnosis = read_patient_diagnosis(record_id, diagnosis_id, db)

    db.delete(diagnosis)
    db.commit()

    return None
