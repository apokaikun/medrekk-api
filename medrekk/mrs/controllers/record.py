from typing import List
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.patient import PatientRecord
from medrekk.mrs.schemas.patients import PatientRecordCreate, PatientRecordUpdate
from medrekk.common.utils import shortid


def create_record(
    account_id: str,
    patient_id: str,
    record: PatientRecordCreate,
    db: Session,
) -> PatientRecord:
    new_record = PatientRecord(**record.model_dump())
    new_record.account_id = account_id
    new_record.patient_id = patient_id
    new_record.id = shortid()

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


def read_records(
    account_id: str,
    patient_id: str,
    db: Session,
) -> List[PatientRecord]:
    records = (
        db.query(PatientRecord)
        .filter(PatientRecord.account_id == account_id)
        .filter(PatientRecord.patient_id == patient_id)
        .order_by(PatientRecord.updated.desc())
        .all()
    )
    return records


def read_record(
    account_id: str,
    patient_id: str,
    record_id,
    db: Session,
) -> PatientRecord:
    record = (
        db.query(PatientRecord)
        .filter(PatientRecord.account_id == account_id)
        .filter(PatientRecord.patient_id == patient_id)
        .filter(PatientRecord.id == record_id)
        .one_or_none()
    )

    return record


def update_record(
    account_id: str,
    patient_id: str,
    record_id: str,
    record: PatientRecordUpdate,
    db: Session,
) -> PatientRecord:
    record_db = read_record(account_id, patient_id, record_id, db)

    for field, value in record.model_dump(exclude_unset=True).items():
        setattr(record_db, field, value)

    db.add(record_db)
    db.commit()
    db.refresh(record_db)

    return record_db

def delete_record(
    account_id: str,
    patient_id: str,
    record_id: str,
    db: Session,
) -> None:
    record = read_record(account_id, patient_id, record_id, db)

    db.delete(record)
    db.commit()

    return None