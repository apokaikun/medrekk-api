from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers import (
    create_patient,
    read_patients,
    read_patient,
    create_patient_bloodpressure,
    read_patient_bloodpressures,
    read_patient_bloodpressure,
    update_patient_bloodpressure,
    delete_patient_bloodpressure,
)
from medrekk.database.connection import get_db
from medrekk.schemas import (
    PatientProfileCreate,
    PatientProfileRead,
    PatientBloodPressureRead,
    PatientBloodPressureCreate,
    PatientBloodPressureUpdate,
    PatientBloodPressureDelete,
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
    validated = []
    for patient in patients:
        _patient = PatientProfileRead.model_validate(patient)
        _patient.url = patient_routes.prefix + f"/{patient.id}"
        validated.append(_patient)

    return validated


@patient_routes.get("/{patient_id}", response_model=PatientProfileRead)
async def get_patient(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    patient = read_patient(patient_id, db)
    patient.url = patient_routes.prefix + f"/{patient_id}"

    return patient


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
    name="Get Patient Blood Pressure"
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
    name="Update Blood Pressure Record"
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