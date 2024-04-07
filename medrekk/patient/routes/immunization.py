from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.patient.controllers.immunization import (
    create_immunization,
    delete_immunization,
    read_immunization,
    read_immunizations,
    update_immunization,
)
from medrekk.common.database.connection import get_db
from medrekk.patient.schemas.patients import (
    PatientImmunizationCreate,
    PatientImmunizationRead,
    PatientImmunizationUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

immunization_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.IMMUNIZATION}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Immunization"],
)


@immunization_routes.post(
    "/",
    response_model=PatientImmunizationRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_immunization(
    patient_id: str,
    immunization: PatientImmunizationCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_immunization = create_immunization(patient_id, immunization, db)

    return new_immunization

@immunization_routes.get(
    "/",
    response_model=List[PatientImmunizationRead],
)
async def get_patient_immunizations(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    immunizations = read_immunizations(patient_id, db)

    return immunizations

@immunization_routes.get(
    "/{immunization_id}",
    response_model=PatientImmunizationRead,
)
async def get_patient_immunization(
    patient_id: str,
    immunization_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    immunization = read_immunization(patient_id, immunization_id, db)

    return immunization

@immunization_routes.put(
    "/{immunization_id}",
    response_model=PatientImmunizationRead,
)
async def update_patient_immunization(
    patient_id: str,
    immunization_id: str,
    immunization: PatientImmunizationUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_immunization = update_immunization(patient_id, immunization_id, immunization, db)

    return updated_immunization

@immunization_routes.delete(
    "/{immunization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_immunization(
    patient_id: str,
    immunization_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_immunization(patient_id, immunization_id, db)