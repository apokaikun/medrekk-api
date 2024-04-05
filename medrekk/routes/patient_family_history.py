from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers.patient_family_history import (
    create_family_history,
    delete_family_history,
    read_family_history,
    update_family_history,
)
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientFamilyHistoryCreate,
    PatientFamilyHistoryRead,
    PatientFamilyHistoryUpdate,
)
from medrekk.utils import routes
from medrekk.utils.auth import verify_jwt_token

family_history_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.FAMILYHISTORY}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Family History"],
)


@family_history_routes.post(
    "/",
    response_model=PatientFamilyHistoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_family_history(
    patient_id: str,
    family_history: PatientFamilyHistoryCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_family_history = create_family_history(patient_id, family_history, db)

    return new_family_history


@family_history_routes.get(
    "/",
    response_model=PatientFamilyHistoryRead,
)
async def get_patient_family_history(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    family_history = read_family_history(patient_id, db)

    return family_history

@family_history_routes.put(
    "/",
    response_model=PatientFamilyHistoryRead,
)
async def update_patient_family_history(
    patient_id: str,
    family_history: PatientFamilyHistoryUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_family_history = update_family_history(patient_id, family_history, db)

    return updated_family_history

@family_history_routes.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_family_history(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_family_history(patient_id, db)