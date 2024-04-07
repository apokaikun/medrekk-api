from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.patient.controllers.diagnosis import (
    create_patient_diagnosis,
    delete_patient_diagnosis,
    read_patient_diagnosis,
    read_patient_diagnoses,
    update_patient_diagnosis,
)
from medrekk.common.database.connection import get_db
from medrekk.patient.schemas.patients import (
    PatientDiagnosisCreate,
    PatientDiagnosisRead,
    PatientDiagnosisUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import account_record_id_validate, verify_jwt_token

diagnosis_routes = APIRouter(
    prefix=f"/{routes.RECORDS}" + "/{record_id}" + f"/{routes.DIAGNOSIS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Diagnosis"],
)

# START: Blood Pressure


@diagnosis_routes.post(
    "/",
    response_model=PatientDiagnosisRead,
    name="Add Patient Blood Pressure",
)
async def add_diagnosis(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    diagnosis: PatientDiagnosisCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_bp = create_patient_diagnosis(record_id, diagnosis, db)

    return PatientDiagnosisRead.model_validate(new_bp)


@diagnosis_routes.get(
    "/",
    response_model=List[PatientDiagnosisRead],
    name="Get Patient Blood Pressures",
)
async def get_diagnoses(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    db: Annotated[Session, Depends(get_db)],
):
    diagnoses = read_patient_diagnoses(record_id, db)

    validated = []
    for bp in diagnoses:
        validated.append(PatientDiagnosisRead.model_validate(bp))

    return validated


@diagnosis_routes.get(
    "/{diagnosis_id}/",
    response_model=PatientDiagnosisRead,
    name="Get Patient Blood Pressure",
)
async def get_diagnosis(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    diagnosis_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    diagnosis = read_patient_diagnosis(record_id, diagnosis_id, db)

    return PatientDiagnosisRead.model_validate(diagnosis)


@diagnosis_routes.put(
    "/{diagnosis_id}",
    response_model=PatientDiagnosisRead,
    name="Update Blood Pressure Record",
)
async def put_diagnosis(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    diagnosis_id: str,
    diagnosis: PatientDiagnosisUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_diagnosis = update_patient_diagnosis(record_id, diagnosis_id, diagnosis, db)

    return PatientDiagnosisRead.model_validate(updated_diagnosis)


@diagnosis_routes.delete(
    "/{diagnosis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_diagnosis(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    diagnosis_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_patient_diagnosis(record_id, diagnosis_id, db)
