from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers.patient_medical_history import (
    create_medical_history,
    delete_medical_history,
    read_medical_history,
    update_medical_history,
)
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientMedicalHistoryCreate,
    PatientMedicalHistoryRead,
    PatientMedicalHistoryUpdate,
)
from medrekk.utils import routes
from medrekk.utils.auth import verify_jwt_token

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
    db: Annotated[Session, Depends(get_db)],
):
    new_medical_history = create_medical_history(patient_id, medical_history, db)

    return new_medical_history


@medical_history_routes.get(
    "/{medical_history_id}",
    response_model=PatientMedicalHistoryRead,
)
async def get_patient_medical_history(
    patient_id: str,
    medical_history_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    medical_history = read_medical_history(patient_id, medical_history_id, db)

    return medical_history


@medical_history_routes.put(
    "/{medical_history_id}",
    response_model=PatientMedicalHistoryRead,
)
async def update_patient_medical_history(
    patient_id: str,
    medical_history_id: str,
    medical_history: PatientMedicalHistoryUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_medical_history = update_medical_history(
        patient_id, medical_history_id, medical_history, db
    )

    return updated_medical_history


@medical_history_routes.delete(
    "/{medical_history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_medical_history(
    patient_id: str,
    medical_history_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_medical_history(patient_id, medical_history_id, db)
