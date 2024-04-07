from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.patient.controllers.ob_history import (
    create_ob_history,
    delete_ob_history,
    read_ob_history,
    update_ob_history,
)
from medrekk.common.database.connection import get_db
from medrekk.patient.schemas.patients import (
    PatientOBHistoryCreate,
    PatientOBHistoryRead,
    PatientOBHistoryUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

ob_history_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.OBHISTROY}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient OB History"],
)


@ob_history_routes.post(
    "/",
    response_model=PatientOBHistoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_ob_history(
    patient_id: str,
    ob_history: PatientOBHistoryCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_ob_history = create_ob_history(patient_id, ob_history, db)

    return new_ob_history


@ob_history_routes.get(
    "/",
    response_model=PatientOBHistoryRead,
)
async def get_patient_ob_history(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    ob_history = read_ob_history(patient_id, db)

    return ob_history


@ob_history_routes.put(
    "/",
    response_model=PatientOBHistoryRead,
)
async def update_patient_ob_history(
    patient_id: str,
    ob_history: PatientOBHistoryUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_ob_history = update_ob_history(
        patient_id, ob_history, db
    )

    return updated_ob_history


@ob_history_routes.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_ob_history(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_ob_history(patient_id, db)
