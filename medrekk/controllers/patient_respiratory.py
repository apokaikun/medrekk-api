from collections import UserDict
from typing import Any, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from medrekk.models import PatientRespiratoryRate as Respiratory
from medrekk.schemas import PatientRespiratoryRateCreate, PatientRespiratoryRateUpdate
from medrekk.utils import shortid


def create_respiratory(
    patient_id: str, respiratory: PatientRespiratoryRateCreate, db: Session
) -> Respiratory:
    new_respiratory = Respiratory(**respiratory.model_dump())
    new_respiratory.id = shortid()

    db.add(new_respiratory)
    db.commit()
    db.refresh(new_respiratory)

    return new_respiratory


def read_respiratories(
    patient_id: str,
    db: Session,
) -> List[Respiratory]:

    respiratories = (
        db.query(Respiratory)
        .filter(Respiratory.patient_id == patient_id)
        .order_by(Respiratory.created.desc())
        .all()
    )

    if not respiratories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient Respiratory Rates NOT FOUND."},
            },
        )
    return respiratories


def read_respiratory(
    patient_id: str,
    respiratory_id: str,
    db: Session,
) -> Respiratory:
    respiratory = (
        db.query(Respiratory)
        .filter(Respiratory['patient_id'] == patient_id)
        .filter(Respiratory.id == respiratory_id)
        .one_or_none()
    )

    if not respiratory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": "Patient Respiratory Rate NOT FOUND."},
            },
        )

    return respiratory


def update_respiratory(
    patient_id: str,
    respiratory_id: str,
    respiratory: PatientRespiratoryRateUpdate,
    db: Session,
) -> Respiratory:

    patient_respiratory = read_respiratory(patient_id, respiratory_id, db)

    for field, value in respiratory.model_dump().items():
        setattr(patient_respiratory, field, value)

    db.add(patient_respiratory)
    db.commit()
    db.refresh(patient_respiratory)

    return patient_respiratory


def delete_repiratory(
    patient_id: str,
    respiratory_id: str,
    db: Session,
) -> None:
    patient_respiratory = read_respiratory(patient_id, respiratory_id, db)
    db.delete(patient_respiratory)
    db.commit()

    return None

# class Filter(UserDict):
#     def __init__(self, field, value) -> None:
#         self.field = field
#         self.value = value

#     def __setitem__(self, key: Any, item: Any) -> None:
#         return super().__setitem__(key, item)
    
#     def __getitem__(self, key: Any) -> Any:
#         return super().__getitem__(key)
    
#     def __
        

# def paginated_query(
#         _type_:type(object), # type: ignore
#         filters:List[]
# )