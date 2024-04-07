from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.patient.controllers.respiratory_rate import (
    create_respiratory,
    delete_respiratory,
    read_respiratories,
    read_respiratory,
    update_respiratory,
)
from medrekk.common.database.connection import get_db
from medrekk.patient.schemas.patients import (
    PatientRespiratoryRateCreate,
    PatientRespiratoryRateRead,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import account_record_id_validate, verify_jwt_token

respiratory_routes = APIRouter(
    prefix=f"/{routes.RECORDS}" + "/{record_id}" + f"/{routes.RESPIRATORYRATES}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Respiratory Rates"],
)


@respiratory_routes.post(
    "/",
    response_model=PatientRespiratoryRateRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_respiratory_rate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    respiratory: PatientRespiratoryRateCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_respiratory = create_respiratory(record_id, respiratory, db)

    return PatientRespiratoryRateRead.model_validate(new_respiratory)


@respiratory_routes.get(
    "/",
    response_model=List[PatientRespiratoryRateRead],
)
async def get_patient_respiratory_rates(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    db: Annotated[Session, Depends(get_db)],
):
    respiratories = read_respiratories(record_id, db)

    return respiratories


@respiratory_routes.get("/{respiratory_id}")
async def get_patient_respiratory_rate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    respiratory_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    respiratory = read_respiratory(record_id, respiratory_id, db)

    return respiratory


@respiratory_routes.put("/{respiratory_id}")
async def update_patient_respiratory_rate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    respiratory_id: str,
    respiratory: PatientRespiratoryRateCreate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_respiratory = update_respiratory(record_id, respiratory_id, respiratory, db)

    return updated_respiratory


@respiratory_routes.delete(
    "/{respiratory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_respiratory_rate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    respiratory_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_respiratory(record_id, respiratory_id, db)
