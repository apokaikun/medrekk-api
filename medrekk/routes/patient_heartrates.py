from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers.patient_heartrate import (
    create_patient_heartrate,
    delete_patient_heartrate,
    read_patient_heartrate,
    read_patient_heartrates,
    update_patient_heartrate,
)
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientHeartRateCreate,
    PatientHeartRateRead,
    PatientHeartRateUpdate,
)
from medrekk.utils import routes
from medrekk.utils.auth import account_record_id_validate, verify_jwt_token

heartrate_routes = APIRouter(
    prefix=f"/{routes.RECORDS}" + "/{record_id}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Heart Rate"],
)

# START: Heart Rate


@heartrate_routes.post(
    "/heartrate/",
    response_model=PatientHeartRateRead,
    status_code=status.HTTP_201_CREATED,
    name="Add Patient Heart Rate",
)
async def add_patient_heartrate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    heartrate: PatientHeartRateCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_heartrate = create_patient_heartrate(record_id, heartrate, db)

    return PatientHeartRateRead.model_validate(new_heartrate)


@heartrate_routes.get(
    "/heartrate/",
    response_model=List[PatientHeartRateRead],
    name="Get Patient Heart Rates",
)
async def get_patient_heartrates(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    db: Annotated[Session, Depends(get_db)],
):
    patient_heartrates = read_patient_heartrates(record_id, db)

    return [
        PatientHeartRateRead.model_validate(heartrate)
        for heartrate in patient_heartrates
    ]


@heartrate_routes.get(
    "/heartrate/{heartrate_id}/",
    response_model=PatientHeartRateRead,
    name="Get Patient Heart Rate",
)
async def get_patient_heartrate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    heartrate_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient_heartrate = read_patient_heartrate(record_id, heartrate_id, db)

    return PatientHeartRateRead.model_validate(patient_heartrate)


@heartrate_routes.put(
    "/heartrate/{heartrate_id}/",
    response_model=PatientHeartRateRead,
    name="Update Patient Heart Rate",
)
async def put_patient_heartrate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    heartrate_id: str,
    heartrate: PatientHeartRateUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_heartrate = update_patient_heartrate(record_id, heartrate_id, heartrate, db)

    return PatientHeartRateRead.model_validate(updated_heartrate)


@heartrate_routes.delete(
    "/heartrate/{heartrate_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Delete Patient Heart Rate",
)
async def delete_heartrate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    heartrate_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_patient_heartrate(record_id, heartrate_id, db)
