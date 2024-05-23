from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.mrs.controllers.allergy import (
    create_allergy,
    delete_allergy,
    read_allergy,
    read_allergies,
    update_allergy,
)
from medrekk.common.database.connection import get_session
from medrekk.mrs.schemas.patients import (
    PatientAllergyCreate,
    PatientAllergyRead,
    PatientAllergyUpdate,
)
from medrekk.common.utils import routes
from medrekk.common.utils.auth import verify_jwt_token

allergy_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.ALLERGY}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Allergy"],
)


@allergy_routes.post(
    "/",
    response_model=PatientAllergyRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_patient_allergy(
    patient_id: str,
    allergy: PatientAllergyCreate,
    db_session: Annotated[Session, Depends(get_session)],
):
    new_allergy = create_allergy(patient_id, allergy, db_session)

    return new_allergy

@allergy_routes.get(
    "/",
    response_model=List[PatientAllergyRead],
)
async def get_patient_hospitalization_histories(
    patient_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    hospitalization_histories = read_allergies(patient_id, db_session)

    return hospitalization_histories

@allergy_routes.get(
    "/{allergy_id}",
    response_model=PatientAllergyRead,
)
async def get_patient_allergy(
    patient_id: str,
    allergy_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    allergy = read_allergy(patient_id, allergy_id, db_session)

    return allergy

@allergy_routes.put(
    "/{allergy_id}",
    response_model=PatientAllergyRead,
)
async def update_patient_allergy(
    patient_id: str,
    allergy_id: str,
    allergy: PatientAllergyUpdate,
    db_session: Annotated[Session, Depends(get_session)],
):
    updated_allergy = update_allergy(patient_id, allergy_id, allergy, db_session)

    return updated_allergy

@allergy_routes.delete(
    "/{allergy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_patient_allergy(
    patient_id: str,
    allergy_id: str,
    db_session: Annotated[Session, Depends(get_session)],
):
    return delete_allergy(patient_id, allergy_id, db_session)