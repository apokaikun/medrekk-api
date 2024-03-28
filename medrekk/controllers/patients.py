from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from medrekk.models import PatientBloodPressure, PatientHeartRate, PatientProfile
from medrekk.schemas import (
    PatientBloodPressureCreate,
    PatientBloodPressureUpdate,
    PatientHeartRateCreate,
    PatientHeartRateDelete,
    PatientHeartRateRead,
    PatientHeartRateUpdate,
    PatientProfileCreate,
    PatientProfileRead,
)
from medrekk.utils import shortid


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
) -> List[Optional[PatientProfile]]:
    try:
        stmt = select(PatientProfile)
        patients = db.scalars(statement=stmt).all()

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
) -> Optional[PatientProfileRead]:
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
    return PatientProfileRead.model_validate(patient)


def update_patient(patient_id: str, db: Session):
    pass


def create_patient_bloodpressure(
    patient_id: str,
    patient_bp: PatientBloodPressureCreate,
    db: Session,
):
    new_bp = PatientBloodPressure(**patient_bp.model_dump())
    new_bp.patient_id = patient_id
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


def read_patient_bloodpressure(
    patient_id: str,
    bp_id: str,
    db: Session,
) -> PatientBloodPressure:
    # stmt = select(PatientBloodPressure).where(
    #     (PatientBloodPressure.patient_id == patient_id)
    #     & (PatientBloodPressure.id == bp_id)
    # )

    # patient_bp = db.scalars(statement=stmt).first()

    patient_bp = db.query(PatientBloodPressure).filter(PatientBloodPressure.patient_id == patient_id).filter(PatientBloodPressure.id == bp_id).one_or_none()

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

        for field, value in bp.model_dump().items():
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

    db.delete(patient_bp)
    db.commit()

    return None


def create_patient_heartrate(
    patient_id: str,
    heartrate: PatientHeartRateCreate,
    db: Session,
) -> PatientHeartRate:
    new_heartrate = PatientHeartRate(**heartrate.model_dump())
    new_heartrate.patient_id = patient_id
    new_heartrate.id = shortid()

    db.add(new_heartrate)
    db.commit()
    db.refresh(new_heartrate)

    return new_heartrate


def read_patient_heartrate(
    patient_id: str,
    heartrate_id: str,
    db: Session,
) -> PatientHeartRate:
    patient_heartrate = (
        db.query(PatientHeartRate)
        .filter(PatientHeartRate.patient_id == patient_id)
        .filter(PatientHeartRate.id == heartrate_id)
        .one_or_none()
    )

    if not patient_heartrate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": f"Heart rate data NOT FOUND."},
            },
        )

    return patient_heartrate


def read_patient_heartrates(
    patient_id: str,
    db: Session,
) -> List[PatientHeartRate]:
    patient_heartrates = (
        db.query(PatientHeartRate)
        .filter(PatientHeartRate.patient_id == patient_id)
        .all()
    )

    return patient_heartrates


def update_patient_heartrate(
    patient_id: str,
    heartrate_id: str,
    heartrate: PatientHeartRateUpdate,
    db: Session,
) -> PatientHeartRate:
    patient_heartrate = (
        db.query(PatientHeartRate)
        .filter(PatientHeartRate.patient_id == patient_id)
        .filter(PatientHeartRate.id == heartrate_id)
        .one_or_none()
    )

    if not patient_heartrate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": f"Heart rate data NOT FOUND."},
            },
        )

    for field, value in heartrate.model_dump().items():
        setattr(patient_heartrate, field, value)

    db.add(patient_heartrate)
    db.commit()
    db.refresh(patient_heartrate)

    return patient_heartrate


def delete_patient_heartrate(
    patient_id: str,
    heartrate_id: str,
    db: Session,
) -> None:
    patient_heartrate = read_patient_heartrate(patient_id, heartrate_id, db)

    db.delete(patient_heartrate)
    db.commit()

    return None
