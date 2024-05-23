from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.mrs.controllers.medical_history import (
    create_medical_history,
    delete_medical_history,
    read_medical_history,
    update_medical_history,
)
from medrekk.common.database.connection import get_session
from medrekk.mrs.schemas.patients import (
    PatientMedicalHistoryCreate,
    PatientMedicalHistoryRead,
    PatientMedicalHistoryUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

medical_history_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.MEDICALHISTROY}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Medical History"],
)


@medical_history_routes.post(
    "/",
    response_model=PatientMedicalHistoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_medical_history(
    patient_id: str,
    medical_history: PatientMedicalHistoryCreate,
    db_session: Annotated[Session, Depends(get_session)],
):
    new_medical_history = create_medical_history(
        patient_id, medical_history, db_session
    )

    return new_medical_history


@medical_history_routes.get(
    "/",
    response_model=PatientMedicalHistoryRead,
)
async def get_patient_medical_history(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    medical_history = read_medical_history(patient_id, db_session)

    return medical_history


@medical_history_routes.put(
    "/",
    response_model=PatientMedicalHistoryRead,
)
async def update_patient_medical_history(
    patient_id: str,
    medical_history: PatientMedicalHistoryUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_medical_history = update_medical_history(
        patient_id, medical_history, db_session
    )

    return updated_medical_history


@medical_history_routes.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_medical_history(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_medical_history(patient_id, db_session)
