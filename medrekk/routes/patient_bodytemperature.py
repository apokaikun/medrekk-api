from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers import create_bodytemperature, read_bodytemperatures
from medrekk.database.connection import get_db
from medrekk.schemas import (
    PatientBodyTemperatureCreate,
    PatientBodyTemperatureRead,
    PatientBodyTemperatureUpdate,
)
from medrekk.utils.auth import verify_jwt_token

bodytemperature_routes = APIRouter(
    prefix="/patients",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Body Temperature"],
)


@bodytemperature_routes.post(
    "/{patient_id}/bodytemperature/",
    response_model=PatientBodyTemperatureRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_body_temperature(
    patient_id: str,
    temperature: PatientBodyTemperatureCreate,
    db: Annotated[Session, Depends(get_db)],
):
    body_temperature = create_bodytemperature(patient_id, temperature, db)

    return PatientBodyTemperatureRead.model_validate(body_temperature)


@bodytemperature_routes.get(
    "/{patient_id}/bodytemperature/", response_model=List[PatientBodyTemperatureRead]
)
async def read_patient_body_temperatures(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    body_temperatures = read_bodytemperatures(patient_id, db)

    return [
        PatientBodyTemperatureRead.model_validate(body_temperature)
        for body_temperature in body_temperatures
    ]
