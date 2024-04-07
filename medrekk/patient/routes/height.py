from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.common.database.connection import get_db
from medrekk.patient.controllers.height import create_height, delete_height, read_height, read_heights, update_height
from medrekk.patient.schemas.patients import (
    PatientHeightCreate,
    PatientHeightRead,
    PatientHeightUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

bodyheight_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.HEIGHTS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Height"],
)


@bodyheight_routes.post(
    "/",
    response_model=PatientHeightRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_height(
    patient_id: str,
    height: PatientHeightCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_height = create_height(patient_id, height, db)

    return new_height

@bodyheight_routes.get(
    "/",
    response_model=List[PatientHeightRead],
)
async def get_patient_heights(
    patient_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    heights = read_heights(patient_id, db)

    return heights

@bodyheight_routes.get(
    "/{height_id}",
    response_model=PatientHeightRead,
)
async def get_patient_height(
    patient_id: str,
    height_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    height = read_height(patient_id, height_id, db)

    return height

@bodyheight_routes.put(
    "/{height_id}",
    response_model=PatientHeightRead,
)
async def update_patient_height(
    patient_id: str,
    height_id: str,
    height: PatientHeightUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    updated_height = update_height(patient_id, height_id, height, db)

    return updated_height

@bodyheight_routes.delete(
    "/{height_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_height(
    patient_id: str,
    height_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return delete_height(patient_id, height_id, db)