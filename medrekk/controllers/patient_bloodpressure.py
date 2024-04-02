from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.models.patient import PatientBloodPressure
from medrekk.schemas.patients import PatientBloodPressureCreate, PatientBloodPressureUpdate
from medrekk.utils import shortid


def create_patient_bloodpressure(
    record_id: str,
    patient_bp: PatientBloodPressureCreate,
    db: Session,
) -> PatientBloodPressure:
    try:
        new_bp = PatientBloodPressure(**patient_bp.model_dump())
        new_bp.record_id = record_id
        new_bp.id = shortid()
        db.add(new_bp)
        db.commit()
        db.refresh(new_bp)

        if not new_bp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
            )

        return new_bp
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("uc_bloodpressure_patient_dt"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": f"Patient cannot have multiple measurements for the same date and time. Date/Time: {new_bp.dt_measured}"
                        },
                    },
                )
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


def read_patient_bloodpressure(
    patient_id: str,
    bp_id: str,
    db: Session,
) -> PatientBloodPressure:

    patient_bp = (
        db.query(PatientBloodPressure)
        .filter(PatientBloodPressure.patient_id == patient_id)
        .filter(PatientBloodPressure.id == bp_id)
        .one_or_none()
    )

    if not patient_bp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Blood pressure data NOT FOUND.",
                },
            },
        )
    return patient_bp


def read_patient_bloodpressures(
    patient_id: str,
    db: Session,
) -> List[PatientBloodPressure]:
    try:
        patient_bps = (
            db.query(PatientBloodPressure)
            .filter(PatientBloodPressure.patient_id == patient_id)
            .order_by(PatientBloodPressure.created.desc())
            .all()
        )
        return patient_bps
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


def update_patient_bloodpressure(
    patient_id: str,
    bp_id: str,
    bp: PatientBloodPressureUpdate,
    db: Session,
) -> PatientBloodPressure:
    try:
        patient_bp = read_patient_bloodpressure(patient_id, bp_id, db)

        for field, value in bp.model_dump(exclude_unset=True).items():
            setattr(patient_bp, field, value)

        db.add(patient_bp)
        db.commit()
        db.refresh(patient_bp)

        return patient_bp
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


def delete_patient_bloodpressure(
    patient_id: str,
    bp_id: str,
    db: Session,
) -> None:
    try:
        patient_bp = read_patient_bloodpressure(patient_id, bp_id, db)

        db.delete(patient_bp)
        db.commit()

        return None
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
