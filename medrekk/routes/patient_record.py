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
from medrekk.utils.auth import get_account_id, verify_jwt_token

record_routes = APIRouter(
    prefix="/patients",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Body Temperature"],
)

@record_routes.post(
    "/patients/{patient_id}/records/",
)
async def add_patient_record(
    patient_id: str,
    account_id: Annotated[str, Depends(get_account_id)]
):
    pass