from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field


class RecordBase(BaseModel):
    id: str
    created: datetime = datetime.now()
    updated: datetime = datetime.now()

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

class RecordCreate(BaseModel):
    chief_complaint: List[str]

class RecordRead(RecordCreate, RecordBase):
    account_id: str
    patient_id: str

class RecordUpdate(RecordCreate):
    pass

class RecordDelete():
    pass