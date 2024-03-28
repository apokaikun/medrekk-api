from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers import (
    create_respiratory,
    read_respiratories,
    read_respiratory,
    update_respiratory,
    delete_repiratory,
)
from medrekk.database.connection import get_db
from medrekk.schemas import (
    PatientRespiratoryRateCreate,
    PatientRespiratoryRateRead,
    PatientRespiratoryRateUpdate,
    PatientRespiratoryRateDelete,
)
from medrekk.utils.auth import verify_jwt_token

respiratory_routes = APIRouter(
    prefix="/patients",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Respiratory"],
)


@respiratory_routes.post(
    "/{patient_id}/respiratory/",
    response_model=PatientRespiratoryRateRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_respiratory_rate(
    patient_id: str,
    respiratory: PatientRespiratoryRateCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_respiratory = create_respiratory(patient_id, respiratory, db)

    return PatientRespiratoryRateRead.model_validate(new_respiratory)


@respiratory_routes.get(
    "/{patient_id}/respiratory",
    response_model=List[PatientRespiratoryRateRead],
)
async def get_patient_respiratory_rates(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    respiratories = read_respiratories(patient_id, db)

    return [
        PatientRespiratoryRateRead.model_validate(respiratory)
        for respiratory in respiratories
    ]


@respiratory_routes.get(
    "/{patient_id}/respiratory/{respiratory_id}/",
    response_model=PatientRespiratoryRateRead,
)
async def get_patient_respiratory_rate(
    patient_id: str,
    respiratory_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    respiratory = get_patient_respiratory_rate(patient_id, respiratory_id, db)

    return PatientRespiratoryRateRead.model_validate(respiratory)


@respiratory_routes.put(
    "/{patient_id}/respiratory/{respiratory_id}/",
    response_model=PatientRespiratoryRateRead,
)
async def update_patient_respiratory_rate(
    patient_id: str,
    respiratory_id: str,
    respiratory: PatientRespiratoryRateUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    respiratory = update_respiratory(patient_id, respiratory_id, respiratory, db)

    return PatientRespiratoryRateRead.model_validate(respiratory)

@respiratory_routes.delete(
    "/{patient_id}/respiratory/{respiratory_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_respiratory_rate(
    patient_id: str,
    respiratory_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_repiratory(patient_id, respiratory_id, db)