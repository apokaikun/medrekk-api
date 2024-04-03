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
from medrekk.utils.auth import account_record_id_validate, verify_jwt_token

bloodpressure_routes = APIRouter(
    prefix=f"/{routes.RECORDS}" + "/{record_id}" + f"/{routes.BLOODPRESSURES}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Blood Pressure"],
)

# START: Blood Pressure


@bloodpressure_routes.post(
    "/",
    response_model=PatientBloodPressureRead,
    name="Add Patient Blood Pressure",
)
async def add_bloodpressure(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    patient_bp: PatientBloodPressureCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_bp = create_patient_bloodpressure(record_id, patient_bp, db)

    return PatientBloodPressureRead.model_validate(new_bp)


@bloodpressure_routes.get(
    "/",
    response_model=List[PatientBloodPressureRead],
    name="Get Patient Blood Pressures",
)
async def get_bloodpressures(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    db: Annotated[Session, Depends(get_db)],
):
    patient_bps = read_patient_bloodpressures(record_id, db)

    validated = []
    for bp in patient_bps:
        validated.append(PatientBloodPressureRead.model_validate(bp))

    return validated


@bloodpressure_routes.get(
    "/{bp_id}/",
    response_model=PatientBloodPressureRead,
    name="Get Patient Blood Pressure",
)
async def get_bloodpressure(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bp_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient_bp = read_patient_bloodpressure(record_id, bp_id, db)

    return PatientBloodPressureRead.model_validate(patient_bp)


@bloodpressure_routes.put(
    "/{bp_id}",
    response_model=PatientBloodPressureRead,
    name="Update Blood Pressure Record",
)
async def put_bloodpressure(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bp_id: str,
    bp: PatientBloodPressureUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    patient_bp = update_patient_bloodpressure(record_id, bp_id, bp, db)

    return PatientBloodPressureRead.model_validate(patient_bp)


@bloodpressure_routes.delete(
    "/{bp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bloodpressure(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bp_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_patient_bloodpressure(record_id, bp_id, db)


# END : Blood Pressure
