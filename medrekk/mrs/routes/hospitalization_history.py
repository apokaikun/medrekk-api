from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.mrs.controllers.hospitalization_history import (
    create_hospitalization_history,
    delete_hospitalization_history,
    read_hospitalization_history,
    read_hospitalization_histories,
    update_hospitalization_history,
)
from medrekk.common.database.connection import get_session
from medrekk.mrs.schemas.patients import (
    PatientHospitalizationHistoryCreate,
    PatientHospitalizationHistoryRead,
    PatientHospitalizationHistoryUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

hospitalization_history_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}"
    + "/{patient_id}"
    + f"/{routes.HOSPITALIZATIONHISTORY}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Hospitalization History"],
)


@hospitalization_history_routes.post(
    "/",
    response_model=PatientHospitalizationHistoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_hospitalization_history(
    patient_id: str,
    hospitalization_history: PatientHospitalizationHistoryCreate,
    db_session: Annotated[Session, Depends(get_session)],
):
    new_hospitalization_history = create_hospitalization_history(
        patient_id,
        hospitalization_history,
        db_session,
    )

    return new_hospitalization_history


@hospitalization_history_routes.get(
    "/",
    response_model=List[PatientHospitalizationHistoryRead],
)
async def get_patient_hospitalization_histories(
    patient_id: str, db_session: Annotated[Session, Depends(get_session)]
):
    hospitalization_histories = read_hospitalization_histories(patient_id, db_session)

    return hospitalization_histories


@hospitalization_history_routes.get(
    "/{hospitalization_history_id}",
    response_model=PatientHospitalizationHistoryRead,
)
async def get_patient_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    hospitalization_history = read_hospitalization_history(
        patient_id, hospitalization_history_id, db_session
    )

    return hospitalization_history


@hospitalization_history_routes.put(
    "/{hospitalization_history_id}",
    response_model=PatientHospitalizationHistoryRead,
)
async def update_patient_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    hospitalization_history: PatientHospitalizationHistoryUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_hospitalization_history = update_hospitalization_history(
        patient_id,
        hospitalization_history_id,
        hospitalization_history,
        db_session,
    )

    return updated_hospitalization_history


@hospitalization_history_routes.delete(
    "/{hospitalization_history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_hospitalization_history(
        patient_id, hospitalization_history_id, db_session
    )
