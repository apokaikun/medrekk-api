from pydantic import BaseModel


class RESPONSE_CONTENT(BaseModel):
    msg: str
    loc: str


class HTTP_EXCEPTION(BaseModel):
    status_code: int
    content: RESPONSE_CONTENT
