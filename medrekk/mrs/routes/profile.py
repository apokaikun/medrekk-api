from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from medrekk.common.database.connection import get_session
from medrekk.common.utils.auth import verify_jwt_token
from medrekk.mrs.controllers.profile import create_patient, read_patient, read_patients
from medrekk.mrs.schemas.patients import PatientProfileCreate, PatientProfileRead

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
    db_session: Annotated[Session, Depends(get_session)],
):
    new_patient = create_patient(patient, db_session)

    return PatientProfileRead.model_validate(new_patient)


@patient_routes.get(
    "/",
    response_model=List[PatientProfileRead],
    name="Patient profiles list",
    responses={},
)
async def list_patients(
    db_session: Annotated[Session, Depends(get_session)],
):
    patients = read_patients(db_session)

    return [PatientProfileRead.model_validate(patient) for patient in patients]


@patient_routes.get(
    "/{patient_id}",
    response_model=PatientProfileRead,
)
async def get_patient(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    patient = read_patient(patient_id, db_session)

    return PatientProfileRead.model_validate(patient)


# @patient_routes.put(
#     "/{patient_id}",
#     name="Update patient profile",
#     response_model=PatientProfileRead,
# )
async def put_patient(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    pass


# Only self can delete.
# @patient_routes.delete(
#     "/{patient_id}",
#     name="Delete patient",
# )
async def delete_patient(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    pass
