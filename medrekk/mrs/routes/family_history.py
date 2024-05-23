from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.mrs.controllers.family_history import (
    create_family_history,
    delete_family_history,
    read_family_history,
    update_family_history,
)
from medrekk.common.database.connection import get_db, get_session
from medrekk.mrs.schemas.patients import (
    PatientFamilyHistoryCreate,
    PatientFamilyHistoryRead,
    PatientFamilyHistoryUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

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
    db_session: Annotated[Session, Depends(get_session)],
):
    new_family_history = create_family_history(patient_id, family_history, db_session)

    return new_family_history


@family_history_routes.get(
    "/",
    response_model=PatientFamilyHistoryRead,
)
async def get_patient_family_history(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    family_history = read_family_history(patient_id, db_session)

    return family_history

@family_history_routes.put(
    "/",
    response_model=PatientFamilyHistoryRead,
)
async def update_patient_family_history(
    patient_id: str,
    family_history: PatientFamilyHistoryUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_family_history = update_family_history(patient_id, family_history, db_session)

    return updated_family_history

@family_history_routes.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_family_history(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_family_history(patient_id, db_session)