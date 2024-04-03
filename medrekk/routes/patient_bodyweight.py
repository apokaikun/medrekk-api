from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.controllers.patient_bodyweight import (
    create_bodyweight,
    read_bodyweight,
    read_bodyweights,
    update_bodyweight,
    delete_bodyweight,
)
from medrekk.database.connection import get_db
from medrekk.schemas.patients import (
    PatientBodyWeightCreate,
    PatientBodyWeightRead,
    PatientBodyWeightUpdate,
    PatientBodyWeightDelete,
)
from medrekk.utils import routes
from medrekk.utils.auth import account_record_id_validate, verify_jwt_token

bodyweight_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.BODYWEIGHTS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Blood Pressure"],
)

@bodyweight_routes.post(
    "/",
    response_model=PatientBodyWeightRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_bodyweight(
    patient_id: str,
    bodyweight: PatientBodyWeightCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_bodyweight = create_bodyweight(patient_id, bodyweight, db)

    return new_bodyweight

@bodyweight_routes.get(
    "/",
    response_model=List[PatientBodyWeightRead],
)
async def get_patient_bodyweights(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    bodyweights = read_bodyweights(patient_id, db)

    return bodyweights

@bodyweight_routes.get(
    "/{bodyweight_id}",
    response_model=PatientBodyWeightRead,
)
async def get_patient_bodyweight(
    patient_id: str,
    bodyweight_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    bodyweight = read_bodyweight(patient_id, bodyweight_id, db)

    return bodyweight

@bodyweight_routes.put(
    "/{bodyweight_id}",
    response_model=PatientBodyWeightUpdate
)
async def update_patient_bodyweight(
    patient_id: str,
    bodyweight_id: str,
    bodyweight: PatientBodyWeightUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_bodyweight = update_bodyweight(patient_id, bodyweight_id, bodyweight, db)

    return updated_bodyweight