from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers.patient_medication import (
    create_medication,
    delete_medication,
    read_medication,
    read_medications,
    update_medication,
)
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientMedicationCreate,
    PatientMedicationRead,
    PatientMedicationUpdate,
)
from medrekk.utils import routes
from medrekk.utils.auth import verify_jwt_token

medication_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.MEDICATIONS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Medication"],
)


@medication_routes.post(
    "/",
    response_model=PatientMedicationRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_medication(
    patient_id: str,
    medication: PatientMedicationCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_medication = create_medication(patient_id, medication, db)

    return new_medication

@medication_routes.get(
    "/",
    response_model=List[PatientMedicationRead],
)
async def get_patient_hospitalization_histories(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    hospitalization_histories = read_medications(patient_id, db)

    return hospitalization_histories

@medication_routes.get(
    "/{medication_id}",
    response_model=PatientMedicationRead,
)
async def get_patient_medication(
    patient_id: str,
    medication_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    medication = read_medication(patient_id, medication_id, db)

    return medication

@medication_routes.put(
    "/{medication_id}",
    response_model=PatientMedicationRead,
)
async def update_patient_medication(
    patient_id: str,
    medication_id: str,
    medication: PatientMedicationUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_medication = update_medication(patient_id, medication_id, medication, db)

    return updated_medication

@medication_routes.delete(
    "/{medication_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_medication(
    patient_id: str,
    medication_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_medication(patient_id, medication_id, db)