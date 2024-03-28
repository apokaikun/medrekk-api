from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers import (
    create_patient,
    create_patient_bloodpressure,
    create_patient_heartrate,
    delete_patient_bloodpressure,
    delete_patient_heartrate,
    read_patient,
    read_patient_bloodpressure,
    read_patient_bloodpressures,
    read_patient_heartrate,
    read_patient_heartrates,
    read_patients,
    update_patient_bloodpressure,
    update_patient_heartrate,
)
from medrekk.database.connection import get_db
from medrekk.schemas import (
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

patient_routes = APIRouter(
    prefix="/patients", dependencies=[Depends(verify_jwt_token)], tags=["Patients"]
)


@patient_routes.post(
    "/",
    response_model=PatientProfileRead,
    name="Add new patient",
    status_code=201,
    responses={},
)
async def add_patient(
    patient: PatientProfileCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_patient = create_patient(patient, db)

    return PatientProfileRead.model_validate(new_patient)


@patient_routes.get(
    "/",
    response_model=List[PatientProfileRead],
    name="Patient profiles list",
    responses={},
)
async def list_patients(
    db: Annotated[Session, Depends(get_db)],
):
    patients = read_patients(db)

    return [PatientProfileRead.model_validate(patient) for patient in patients]


@patient_routes.get(
    "/{patient_id}",
    response_model=PatientProfileRead,
)
async def get_patient(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient = read_patient(patient_id, db)

    return PatientProfileRead.model_validate(patient)


# @patient_routes.put(
#     "/{patient_id}",
#     name="Update patient profile",
#     response_model=PatientProfileRead,
# )
async def put_patient(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    pass


# Only self can delete.
# @patient_routes.delete(
#     "/{patient_id}",
#     name="Delete patient",
# )
async def delete_patient(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    pass


# START: Blood Pressure


@patient_routes.post(
    "/{patient_id}/bloodpressure/",
    response_model=PatientBloodPressureRead,
    name="Add Patient Blood Pressure",
)
async def add_patient_bp(
    patient_id: str,
    patient_bp: PatientBloodPressureCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_bp = create_patient_bloodpressure(patient_id, patient_bp, db)

    return PatientBloodPressureRead.model_validate(new_bp)


@patient_routes.get(
    "/{patient_id}/bloodpressure/",
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


@patient_routes.get(
    "/{patient_id}/bloodpressure/{bp_id}/",
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


@patient_routes.put(
    "/{patient_id}/bloodpressure/{bp_id}",
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


@patient_routes.delete(
    "/{patient_id}/bloodpressure/{bp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bloodpressure(
    patient_id: str,
    bp_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_patient_bloodpressure(patient_id, bp_id, db)


# END : Blood Pressure

# START: Heart Rate


@patient_routes.post(
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


@patient_routes.get(
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


@patient_routes.get(
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


@patient_routes.put(
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


@patient_routes.delete(
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
