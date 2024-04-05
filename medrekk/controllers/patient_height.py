from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.models.patient import PatientHeight
from medrekk.schemas.patients import PatientHeightCreate, PatientHeightUpdate
from medrekk.utils import shortid


def create_height(
    patient_id: str,
    height: PatientHeightCreate,
    db: Session,
) -> PatientHeight:
    try:
        new_height = PatientHeight(**height.model_dump())
        new_height.id = shortid()
        new_height.patient_id = patient_id

        db.add(new_height)
        db.commit()
        db.refresh(new_height)

        return new_height
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("uc_height_patient_date") >= 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": "Patient cannot have multiple measurements "
                            "for the same date. Date/Time: "
                            f"{new_height.date_measured}"
                        },
                    },
                )


def read_height(
    patient_id: str,
    height_id: str,
    db: Session,
) -> PatientHeight:
    height_db = (
        db.query(PatientHeight)
        .filter(PatientHeight.patient_id == patient_id)
        .filter(PatientHeight.id == height_id)
        .one_or_none()
    )

    if not height_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient height data NOT FOUND."},
            },
        )

    return height_db


def read_heights(
    patient_id: str,
    db: Session,
) -> List[PatientHeight]:
    heights = (
        db.query(PatientHeight)
        .filter(PatientHeight.patient_id == patient_id)
        .order_by(PatientHeight.created.desc())
        .all()
    )

    return heights


def update_height(
    patient_id: str,
    height_id: str,
    height: PatientHeightUpdate,
    db: Session,
) -> PatientHeight:
    height_db = read_height(patient_id, height_id, db)

    for field, value in height.model_dump(exclude_unset=True).items():
        setattr(height_db, field, value)

    db.add(height_db)
    db.commit()
    db.refresh(height_db)

    return height_db



def delete_height(
    patient_id: str,
    height_id: str,
    db: Session,
) -> None:
    height_db = read_height(patient_id, height_id, db)

    db.delete(height_db)
    db.commit()

    return None

