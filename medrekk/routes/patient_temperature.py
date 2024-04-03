from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from medrekk.database.connection import get_db
from medrekk.utils import routes
from medrekk.utils.auth import account_record_id_validate, verify_jwt_token
from medrekk.schemas.patients import PatientBodyTemperatureCreate, PatientBodyTemperatureRead, PatientBodyTemperatureUpdate
from sqlalchemy.orm import Session
from medrekk.controllers.patient_bodytemp import create_bodytemp, read_bodytemp, read_bodytemps, update_bodytemp, delete_bodytemp
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
    db: Annotated[Session, Depends(get_db)]
):
    new_temp = create_bodytemp(record_id, bodytemp, db)

    return new_temp

@bodytemp_routes.get(
        "/",
        response_model=List[PatientBodyTemperatureRead],
)
async def get_patient_body_temperatures(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    db: Annotated[Session, Depends(get_db)],
) -> PatientBodyTemperatureRead:
    bodytemps = read_bodytemps(record_id, db)

    return bodytemps

@bodytemp_routes.get(
        "/{bodytemp_id}",
        response_model=PatientBodyTemperatureRead
)
async def get_patient_body_temperature(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bodytemp_id: str,
    db: Annotated[Session, Depends(get_db)],
) -> PatientBodyTemperatureRead:
    bodytemp = read_bodytemp(record_id, bodytemp_id, db)

    return bodytemp

@bodytemp_routes.put(
    "/{bodytemp_id}",
    response_model=PatientBodyTemperatureRead,
)
async def update_patient_body_temperature(
    record_id: Annotated[str, Depends(account_record_id_validate)],
    bodytemp_id: str,
    bodytemp: PatientBodyTemperatureUpdate,
    db: Annotated[Session, Depends(get_db)],
):
        updated_bodytemp = update_bodytemp(record_id, bodytemp_id, bodytemp, db)

        return updated_bodytemp

@bodytemp_routes.delete(
     "/{bodytemp_id}",
     status_code=status.HTTP_204_NO_CONTENT
)
async def delete_patient_body_temperature(
     record_id: Annotated[str, Depends(get_db)],
     bodytemp_id: str,
     db: Annotated[Session, Depends(get_db)],
):
     return delete_bodytemp(record_id, bodytemp_id, db)