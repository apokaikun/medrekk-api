from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from medrekk.database.connection import get_db
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.schemas import PatientProfileCreate, PatientProfileRead
from medrekk.utils.auth import get_user_id, verify_jwt_token


patient_routes = APIRouter(
    prefix="/patients",
    dependencies=[Depends(verify_jwt_token)],
)

@patient_routes.post(
    "/",
    response_model=PatientProfileRead
    name="Add new patient",
    status_code=201,
    responses={},
)
async def add_patient(
    patient: PatientProfileCreate,
    db: Annotated[Session, Depends(get_db)],
):
    pass
    # new_patient = create_patient(patient, db)


@patient_routes.get(
    "/",
    response_model=List[PatientProfileRead],
    name="Patient profiles list",
    responses={}
)
async def list_patients(
    db: Annotated[Session, Depends(get_db)],
):
    pass


@patient_routes.get(
    "/{patient_id}",
    response_model=PatientProfileRead
)
async def get_patient(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    pass

@patient_routes.put(
    "/{patient_id}",
    name="Update patient profile"
    response_model=PatientProfileRead

)
async def put_patient(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    pass

# Only self can delete.
@patient_routes.delete(
    "/{patient_id}",
    name="Delete patient"
)
async def delete_patient(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    pass
