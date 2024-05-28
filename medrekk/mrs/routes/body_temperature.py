from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.common.database.connection import get_session
from medrekk.mrs.controllers.body_temperature import (
    create_bodytemp,
    delete_bodytemp,
    read_bodytemp,
    read_bodytemps,
    update_bodytemp,
)
from medrekk.mrs.schemas.patients import (
    PatientBodyTemperatureCreate,
    PatientBodyTemperatureRead,
    PatientBodyTemperatureUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import account_record_id_validate, verify_jwt_token

bodytemp_routes = APIRouter(
    prefix=f"/{routes.RECORDS}" + "/{record_id}" + f"/{routes.BODYTEMPERATURES}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Body Temperature Records"],
)


@bodytemp_routes.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PatientBodyTemperatureRead,
    name="Add body temperature record.",
)
async def add_patient_body_temperature(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bodytemp: PatientBodyTemperatureCreate,
    db_session: Annotated[Session, Depends(get_session)],
):
    new_temp = create_bodytemp(record_id, bodytemp, db_session)

    return new_temp


@bodytemp_routes.get(
    "/",
    response_model=List[PatientBodyTemperatureRead],
)
async def get_patient_body_temperatures(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    db_session: Annotated[Session, Depends(get_session)],
) -> PatientBodyTemperatureRead:
    bodytemps = read_bodytemps(record_id, db_session)

    return bodytemps


@bodytemp_routes.get("/{bodytemp_id}", response_model=PatientBodyTemperatureRead)
async def get_patient_body_temperature(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bodytemp_id: str,
    db_session: Annotated[Session, Depends(get_session)],
) -> PatientBodyTemperatureRead:
    bodytemp = read_bodytemp(record_id, bodytemp_id, db_session)

    return bodytemp


@bodytemp_routes.put(
    "/{bodytemp_id}",
    response_model=PatientBodyTemperatureRead,
)
async def update_patient_body_temperature(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bodytemp_id: str,
    bodytemp: PatientBodyTemperatureUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_bodytemp = update_bodytemp(record_id, bodytemp_id, bodytemp, db_session)

    return updated_bodytemp


@bodytemp_routes.delete("/{bodytemp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient_body_temperature(
    record_id: Annotated[str, Depends(get_session)],
    bodytemp_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_bodytemp(record_id, bodytemp_id, db_session)
