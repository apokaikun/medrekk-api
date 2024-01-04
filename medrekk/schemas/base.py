from datetime import datetime
from typing import Annotated
from pydantic import BaseModel
from shortuuid import uuid


class MedRekkBaseModel(BaseModel):
    id: str = uuid()
    created: datetime = datetime.now()
    updated: datetime = datetime.now()
