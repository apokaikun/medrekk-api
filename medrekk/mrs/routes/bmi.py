from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.mrs.controllers.bmi import (
    create_bmi,
    delete_bmi,
    read_bmi,
    read_bmis,
    update_bmi,
)
from medrekk.common.database.connection import get_session
from medrekk.mrs.schemas.patients import (
    PatientBodyMassIndexCreate,
    PatientBodyMassIndexRead,
    PatientBodyMassIndexUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

bmi_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.BODYMASSINDEX}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient BMI"],
)


@bmi_routes.post(
    "/",
    response_model=PatientBodyMassIndexRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_bmi(
    patient_id: str,
    bmi: PatientBodyMassIndexCreate,
    db_session: Annotated[Session, Depends(get_session)],
):
    new_bmi = create_bmi(patient_id, bmi, db_session)

    return new_bmi

@bmi_routes.get(
    "/",
    response_model=List[PatientBodyMassIndexRead],
)
async def get_patient_bmis(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)]
):
    bmis = read_bmis(patient_id, db_session)

    return bmis

@bmi_routes.get(
    "/{bmi_id}",
    response_model=PatientBodyMassIndexRead,
)
async def get_patient_bmi(
    patient_id: str,
    bmi_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    bmi = read_bmi(patient_id, bmi_id, db_session)

    return bmi

@bmi_routes.put(
    "/{bmi_id}",
    response_model=PatientBodyMassIndexRead,
)
async def update_patient_bmi(
    patient_id: str,
    bmi_id: str,
    bmi: PatientBodyMassIndexUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_bmi = update_bmi(patient_id, bmi_id, bmi, db_session)

    return updated_bmi

@bmi_routes.delete(
    "/{bmi_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_bmi(
    patient_id: str,
    bmi_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_bmi(patient_id, bmi_id, db_session)