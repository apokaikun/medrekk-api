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
from medrekk.controllers.patient_heartrate import (
    create_patient_heartrate,
    delete_patient_heartrate,
    read_patient_heartrate,
    read_patient_heartrates,
    update_patient_heartrate,
)
from medrekk.controllers.patients import create_patient, read_patient, read_patients
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientBloodPressureCreate,
    PatientBloodPressureDelete,
    PatientBloodPressureRead,
    PatientBloodPressureUpdate,
    PatientHeartRateCreate,
    PatientHeartRateDelete,
    PatientHeartRateRead,
    PatientHeartRateUpdate,
    PatientProfileCreate,
    PatientProfileRead,
)
from medrekk.utils.auth import verify_jwt_token

heartrate_routes = APIRouter(
    prefix="/patients", dependencies=[Depends(verify_jwt_token)], tags=["Patient Heart Rate"]
)

# START: Heart Rate


@heartrate_routes.post(
    "/{patient_id}/heartrate/",
    response_model=PatientHeartRateRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_heartrate(
    patient_id: str,
    heartrate: PatientHeartRateCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_heartrate = create_patient_heartrate(patient_id, heartrate, db)

    return PatientHeartRateRead.model_validate(new_heartrate)


@heartrate_routes.get(
    "/{patient_id}/heartrate/",
    response_model=List[PatientHeartRateRead],
    name="Get Patient Heart Rates",
)
async def get_patient_heartrates(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient_heartrates = read_patient_heartrates(patient_id, db)

    return [
        PatientHeartRateRead.model_validate(heartrate)
        for heartrate in patient_heartrates
    ]


@heartrate_routes.get(
    "/{patient_id}/heartrate/{heartrate_id}/",
    response_model=PatientHeartRateRead,
    name="Get Patient Heart Rate",
)
async def get_patient_heartrate(
    patient_id: str,
    heartrate_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient_heartrate = read_patient_heartrate(patient_id, heartrate_id, db)

    return PatientHeartRateRead.model_validate(patient_heartrate)


@heartrate_routes.put(
    "/{patient_id}/heartrate/{heartrate_id}/",
    response_model=PatientHeartRateRead,
    name="Update Patient Heart Rate",
)
async def put_patient_heartrate(
    patient_id: str,
    heartrate_id: str,
    heartrate: PatientHeartRateUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_heartrate = update_patient_heartrate(
        patient_id, heartrate_id, heartrate, db
    )

    return PatientHeartRateRead.model_validate(updated_heartrate)


@heartrate_routes.delete(
    "/{patient_id}/heartrate/{heartrate_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete Patient Heart Rate",
)
async def delete_heartrate(
    patient_id: str,
    heartrate_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_patient_heartrate(patient_id, heartrate_id, db)
