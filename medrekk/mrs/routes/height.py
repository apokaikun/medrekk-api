from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.common.database.connection import get_session
from medrekk.mrs.controllers.height import create_height, delete_height, read_height, read_heights, update_height
from medrekk.mrs.schemas.patients import (
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
    db_session: Annotated[Session, Depends(get_session)],
):
    new_height = create_height(patient_id, height, db_session)

    return new_height

@bodyheight_routes.get(
    "/",
    response_model=List[PatientHeightRead],
)
async def get_patient_heights(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)]
):
    heights = read_heights(patient_id, db_session)

    return heights

@bodyheight_routes.get(
    "/{height_id}",
    response_model=PatientHeightRead,
)
async def get_patient_height(
    patient_id: str,
    height_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    height = read_height(patient_id, height_id, db_session)

    return height

@bodyheight_routes.put(
    "/{height_id}",
    response_model=PatientHeightRead,
)
async def update_patient_height(
    patient_id: str,
    height_id: str,
    height: PatientHeightUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_height = update_height(patient_id, height_id, height, db_session)

    return updated_height

@bodyheight_routes.delete(
    "/{height_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_height(
    patient_id: str,
    height_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_height(patient_id, height_id, db_session)