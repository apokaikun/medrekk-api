from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers.patient_hospitalization_history import (
    create_hospitalization_history,
    delete_hospitalization_history,
    read_hospitalization_history,
    read_hospitalization_histories,
    update_hospitalization_history,
)
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientHospitalizationHistoryCreate,
    PatientHospitalizationHistoryRead,
    PatientHospitalizationHistoryUpdate,
)
from medrekk.utils import routes
from medrekk.utils.auth import verify_jwt_token

hospitalization_history_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.HOSPITALIZATIONHISTORY}",
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
    db: Annotated[Session, Depends(get_db)],
):
    new_hospitalization_history = create_hospitalization_history(patient_id, hospitalization_history, db)

    return new_hospitalization_history

@hospitalization_history_routes.get(
    "/",
    response_model=List[PatientHospitalizationHistoryRead],
)
async def get_patient_hospitalization_histories(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    hospitalization_histories = read_hospitalization_histories(patient_id, db)

    return hospitalization_histories

@hospitalization_history_routes.get(
    "/{hospitalization_history_id}",
    response_model=PatientHospitalizationHistoryRead,
)
async def get_patient_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    hospitalization_history = read_hospitalization_history(patient_id, hospitalization_history_id, db)

    return hospitalization_history

@hospitalization_history_routes.put(
    "/{hospitalization_history_id}",
    response_model=PatientHospitalizationHistoryRead,
)
async def update_patient_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    hospitalization_history: PatientHospitalizationHistoryUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_hospitalization_history = update_hospitalization_history(patient_id, hospitalization_history_id, hospitalization_history, db)

    return updated_hospitalization_history

@hospitalization_history_routes.delete(
    "/{hospitalization_history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_hospitalization_history(
    patient_id: str,
    hospitalization_history_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_hospitalization_history(patient_id, hospitalization_history_id, db)