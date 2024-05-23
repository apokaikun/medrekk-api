from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.common.database.connection import get_session
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token
from medrekk.mrs.controllers.surgical_history import (
    create_surgical_history,
    delete_surgical_history,
    read_surgical_histories,
    read_surgical_history,
    update_surgical_history,
)
from medrekk.mrs.schemas.patients import (
    PatientSurgicalHistoryCreate,
    PatientSurgicalHistoryRead,
    PatientSurgicalHistoryUpdate,
)

surgical_history_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.SURGICALHISTORY}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Surgical History"],
)


@surgical_history_routes.post(
    "/",
    response_model=PatientSurgicalHistoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_surgical_history(
    patient_id: str,
    surgical_history: PatientSurgicalHistoryCreate,
    db_session: Annotated[Session, Depends(get_session)],
):
    new_surgical_history = create_surgical_history(
        patient_id, surgical_history, db_session
    )

    return new_surgical_history


@surgical_history_routes.get(
    "/",
    response_model=List[PatientSurgicalHistoryRead],
)
async def get_patient_surgical_histories(
    patient_id: str, db_session: Annotated[Session, Depends(get_session)]
):
    surgical_histories = read_surgical_histories(patient_id, db_session)

    return surgical_histories


@surgical_history_routes.get(
    "/{surgical_history_id}",
    response_model=PatientSurgicalHistoryRead,
)
async def get_patient_surgical_history(
    patient_id: str,
    surgical_history_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    surgical_history = read_surgical_history(
        patient_id, surgical_history_id, db_session
    )

    return surgical_history


@surgical_history_routes.put(
    "/{surgical_history_id}",
    response_model=PatientSurgicalHistoryRead,
)
async def update_patient_surgical_history(
    patient_id: str,
    surgical_history_id: str,
    surgical_history: PatientSurgicalHistoryUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_surgical_history = update_surgical_history(
        patient_id, surgical_history_id, surgical_history, db_session
    )

    return updated_surgical_history


@surgical_history_routes.delete(
    "/{surgical_history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_surgical_history(
    patient_id: str,
    surgical_history_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_surgical_history(patient_id, surgical_history_id, db_session)
