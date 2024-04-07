from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientBodyMassIndex
from medrekk.patient.schemas.patients import PatientBodyMassIndexCreate, PatientBodyMassIndexUpdate
from medrekk.common.utils import shortid


def create_bmi(
    patient_id: str,
    bmi: PatientBodyMassIndexCreate,
    db: Session,
) -> PatientBodyMassIndex:
    try:
        new_bmi = PatientBodyMassIndex(**bmi.model_dump())
        new_bmi.id = shortid()
        new_bmi.patient_id = patient_id

        db.add(new_bmi)
        db.commit()
        db.refresh(new_bmi)

        return new_bmi
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("uc_bmi_patient_date") >= 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient cannot have multiple measurements "
                            "for the same date. Date/Time: "
                            f"{new_bmi.date_measured}"
                        },
                    },
                )


def read_bmi(
    patient_id: str,
    bmi_id: str,
    db: Session,
) -> PatientBodyMassIndex:
    bmi_db = (
        db.query(PatientBodyMassIndex)
        .filter(PatientBodyMassIndex.patient_id == patient_id)
        .filter(PatientBodyMassIndex.id == bmi_id)
        .one_or_none()
    )

    if not bmi_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient bmi data NOT FOUND."},
            },
        )

    return bmi_db


def read_bmis(
    patient_id: str,
    db: Session,
) -> List[PatientBodyMassIndex]:
    bmis = (
        db.query(PatientBodyMassIndex)
        .filter(PatientBodyMassIndex.patient_id == patient_id)
        .order_by(PatientBodyMassIndex.created.desc())
        .all()
    )

    return bmis


def update_bmi(
    patient_id: str,
    bmi_id: str,
    bmi: PatientBodyMassIndexUpdate,
    db: Session,
) -> PatientBodyMassIndex:
    bmi_db = read_bmi(patient_id, bmi_id, db)

    for field, value in bmi.model_dump(exclude_unset=True).items():
        setattr(bmi_db, field, value)

    db.add(bmi_db)
    db.commit()
    db.refresh(bmi_db)

    return bmi_db



def delete_bmi(
    patient_id: str,
    bmi_id: str,
    db: Session,
) -> None:
    bmi_db = read_bmi(patient_id, bmi_id, db)

    db.delete(bmi_db)
    db.commit()

    return None

