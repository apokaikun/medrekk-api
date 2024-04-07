from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from medrekk.patient.controllers.profile import create_patient, read_patient, read_patients
from medrekk.common.database.connection import get_db
from medrekk.patient.schemas.patients import PatientProfileCreate, PatientProfileRead
from medrekk.common.utils.auth import get_account_id, verify_jwt_token

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
