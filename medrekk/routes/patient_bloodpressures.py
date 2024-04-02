from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers.patient_bloodpressure import (
    create_patient_bloodpressure,
    delete_patient_bloodpressure,
    read_patient_bloodpressure,
    read_patient_bloodpressures,
    update_patient_bloodpressure,
)
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientBloodPressureCreate,
    PatientBloodPressureRead,
    PatientBloodPressureUpdate,
)
from medrekk.utils import routes
from medrekk.utils.auth import is_account_record, verify_jwt_token

bloodpressure_routes = APIRouter(
    prefix=f"/{routes.RECORDS}" + "/{record_id}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Blood Pressure"],
)

# START: Blood Pressure


@bloodpressure_routes.post(
    "/bloodpressure/",
    response_model=PatientBloodPressureRead,
    name="Add Patient Blood Pressure",
)
async def add_bloodpressure(
    record_id: Annotated[str, Depends(is_account_record)],
    patient_bp: PatientBloodPressureCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_bp = create_patient_bloodpressure(record_id, patient_bp, db)

    return PatientBloodPressureRead.model_validate(new_bp)


@bloodpressure_routes.get(
    "/bloodpressure/",
    response_model=List[PatientBloodPressureRead],
    name="Get Patient Blood Pressure Records",
)
def get_bloodpressures(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient_bps = read_patient_bloodpressures(patient_id, db)

    validated = []
    for bp in patient_bps:
        validated.append(PatientBloodPressureRead.model_validate(bp))

    return validated


@bloodpressure_routes.get(
    "/bloodpressure/{bp_id}/",
    response_model=PatientBloodPressureRead,
    name="Get Patient Blood Pressure",
)
def get_bloodpressure(
    patient_id: str,
    bp_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient_bp = read_patient_bloodpressure(patient_id, bp_id, db)

    return PatientBloodPressureRead.model_validate(patient_bp)


@bloodpressure_routes.put(
    "/bloodpressure/{bp_id}",
    response_model=PatientBloodPressureRead,
    name="Update Blood Pressure Record",
)
def put_bloodpressure(
    patient_id: str,
    bp_id: str,
    bp: PatientBloodPressureUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    patient_bp = update_patient_bloodpressure(
        patient_id,
        bp_id,
        bp,
        db,
    )

    return PatientBloodPressureRead.model_validate(patient_bp)


@bloodpressure_routes.delete(
    "/bloodpressure/{bp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bloodpressure(
    patient_id: str,
    bp_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_patient_bloodpressure(patient_id, bp_id, db)


# END : Blood Pressure
