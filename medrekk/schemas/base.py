from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MedRekkBaseSchema(BaseModel):
    id: str 
    created: datetime 
    updated: datetime 

    model_config = ConfigDict(
        from_attributes = True,
        validate_assignment = True,
        arbitrary_types_allowed = True
        )