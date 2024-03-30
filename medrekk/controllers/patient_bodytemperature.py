from typing import List
from fastapi import HTTPException, status
from medrekk.models import PatientBodyTemperature, PatientProfile
from medrekk.schemas import PatientBodyTemperatureCreate, PatientBodyTemperatureRead
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from psycopg.errors import UniqueViolation
from medrekk.utils import shortid


def create_bodytemperature(
    patient_id: str,
    temparature: PatientBodyTemperatureCreate,
    db: Session,
) -> PatientBodyTemperatureRead:
    try:
        body_temperature = PatientBodyTemperature(**temparature.model_dump())
        body_temperature.patient_id = patient_id
        body_temperature.id = shortid()

        db.add(body_temperature)
        db.commit()
        db.refresh(body_temperature)

        return body_temperature
    except DBAPIError as e:
        if isinstance(e.orig, UniqueViolation):
            args: str = e.orig.args[0]
            if args.find("uc_bodytemperature_patient_dt"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "status_code": status.HTTP_409_CONFLICT,
                        "content": {
                            "msg": f"Patient cannot have multiple measurements for the same date and time. Date/Time: {body_temperature.dt_measured}"
                        },
                    },
                )


def read_bodytemperatures(
    patient_id: str, db: Session
) -> List[PatientBodyTemperatureRead]:
    # body_temperatures = db.query(PatientProfile).filter(PatientProfile.id == patient_id).one_or_none()
    body_temperatures = db.query(PatientBodyTemperature).filter(PatientBodyTemperature.patient_id == patient_id).order_by(PatientBodyTemperature.created.desc()).all()
    return body_temperatures
