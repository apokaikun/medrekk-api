from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from medrekk.patient.controllers.record import (
    create_record,
    delete_record,
    read_record,
    read_records,
    update_record,
)
from medrekk.common.database.connection import get_db
from medrekk.patient.schemas.patients import PatientRecordCreate, PatientRecordRead, PatientRecordUpdate
from medrekk.common.utils import routes
from medrekk.common.utils.auth import get_account_id, verify_jwt_token

record_routes = APIRouter(
    prefix=f"/{routes.PATIENTS}" + "/{patient_id}" + f"/{routes.RECORDS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Patient Records"],
)


@record_routes.post(
    "/",
    response_model=PatientRecordRead,
    status_code=status.HTTP_201_CREATED,
    name="Add New Patient Record",
)
async def add_record(
    patient_id: str,
    account_id: Annotated[str, Depends(get_account_id)],
    record: PatientRecordCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_record = create_record(account_id, patient_id, record, db)

    return new_record


@record_routes.get(
    "/",
    response_model=List[PatientRecordRead | None],
    name="Get Patient Records",
)
async def get_records(
    patient_id: str,
    account_id: Annotated[str, Depends(get_account_id)],
    db: Annotated[Session, Depends(get_db)],
):
    records = read_records(account_id, patient_id, db)

    return [PatientRecordRead.model_validate(record) for record in records]


@record_routes.get(
    "/{record_id}",
    response_model=PatientRecordRead,
    name="Get Patient Record",
)
async def get_record(
    patient_id: str,
    record_id: str,
    account_id: Annotated[str, Depends(get_account_id)],
    db: Annotated[Session, Depends(get_db)],
):
    record = read_record(account_id, patient_id, record_id, db)

    return PatientRecordRead.model_validate(record)


@record_routes.put(
    "/{record_id}",
    response_model=PatientRecordRead,
    name="Update Patient Record",
)
async def put_record(
    patient_id: str,
    record_id: str,
    record: PatientRecordUpdate,
    account_id: Annotated[str, Depends(get_account_id)],
    db: Annotated[Session, Depends(get_db)],
):
    updated_record = update_record(account_id, patient_id, record_id, record, db)

    return PatientRecordRead.model_validate(updated_record)


@record_routes.delete(
    "/{record_id}",
    name="Delete Patient Record",
)
async def put_record(
    patient_id: str,
    record_id: str,
    account_id: Annotated[str, Depends(get_account_id)],
    db: Annotated[Session, Depends(get_db)],
):
    return delete_record(account_id, patient_id, record_id, db)
