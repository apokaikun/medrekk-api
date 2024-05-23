from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.common.database.connection import get_session
from medrekk.common.utils import routes
from medrekk.common.utils.auth import account_record_id_validate, verify_jwt_token
from medrekk.mrs.controllers.respiratory_rate import (
    create_respiratory,
    delete_respiratory,
    read_respiratories,
    read_respiratory,
    update_respiratory,
)
from medrekk.mrs.schemas.patients import (
    PatientRespiratoryRateCreate,
    PatientRespiratoryRateRead,
)

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
    db_session: Annotated[Session, Depends(get_session)],
):
    new_respiratory = create_respiratory(record_id, respiratory, db_session)

    return PatientRespiratoryRateRead.model_validate(new_respiratory)


@respiratory_routes.get(
    "/",
    response_model=List[PatientRespiratoryRateRead],
)
async def get_patient_respiratory_rates(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    db_session: Annotated[Session, Depends(get_session)],
):
    respiratories = read_respiratories(record_id, db_session)

    return respiratories


@respiratory_routes.get("/{respiratory_id}")
async def get_patient_respiratory_rate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    respiratory_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    respiratory = read_respiratory(record_id, respiratory_id, db_session)

    return respiratory


@respiratory_routes.put("/{respiratory_id}")
async def update_patient_respiratory_rate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    respiratory_id: str,
    respiratory: PatientRespiratoryRateCreate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_respiratory = update_respiratory(
        record_id, respiratory_id, respiratory, db_session
    )

    return updated_respiratory


@respiratory_routes.delete(
    "/{respiratory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_respiratory_rate(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    respiratory_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_respiratory(record_id, respiratory_id, db_session)
