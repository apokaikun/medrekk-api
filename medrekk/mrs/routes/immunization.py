from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.mrs.controllers.immunization import (
    create_immunization,
    delete_immunization,
    read_immunization,
    read_immunizations,
    update_immunization,
)
from medrekk.common.database.connection import get_session
from medrekk.mrs.schemas.patients import (
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
    db_session: Annotated[Session, Depends(get_session)],
):
    new_immunization = create_immunization(patient_id, immunization, db_session)

    return new_immunization


@immunization_routes.get(
    "/",
    response_model=List[PatientImmunizationRead],
)
async def get_patient_immunizations(
    patient_id: str, db_session: Annotated[Session, Depends(get_session)]
):
    immunizations = read_immunizations(patient_id, db_session)

    return immunizations


@immunization_routes.get(
    "/{immunization_id}",
    response_model=PatientImmunizationRead,
)
async def get_patient_immunization(
    patient_id: str,
    immunization_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    immunization = read_immunization(patient_id, immunization_id, db_session)

    return immunization


@immunization_routes.put(
    "/{immunization_id}",
    response_model=PatientImmunizationRead,
)
async def update_patient_immunization(
    patient_id: str,
    immunization_id: str,
    immunization: PatientImmunizationUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_immunization = update_immunization(
        patient_id,
        immunization_id,
        immunization,
        db_session,
    )

    return updated_immunization


@immunization_routes.delete(
    "/{immunization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_immunization(
    patient_id: str,
    immunization_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_immunization(patient_id, immunization_id, db_session)
