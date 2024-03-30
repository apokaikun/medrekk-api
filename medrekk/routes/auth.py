from pprint import pprint
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, Path, Request
from fastapi.security import APIKeyHeader, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from medrekk.controllers.auth import authenticate_member
from medrekk.database.connection import get_db
from medrekk.routes import *
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.schemas.token import Token
from medrekk.utils.auth import generate_access_token
from medrekk.utils.constants import VERSION, VERSION_SUFFIX

auth_routes = APIRouter(tags=["Authentication"])

# api_key_header = APIKeyHeader(name="X-API-Key")

@auth_routes.post(
    f"/{VERSION}-{VERSION_SUFFIX}/auth",
    response_model=Token,
    status_code=200,
    description="Successful username and password authentication.",
    responses={
        401: {
            "description": "This message indicates that you tried to access a resource that requires authorization, but your credentials (username and password) were not recognized by the server.",
            "model": HTTP_EXCEPTION,
        },
        500: {
            "description": "HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            "model": HTTP_EXCEPTION,
        },
    },
)
def auth(
    host: Annotated[str, Header()],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    pprint(host)
    access_token = authenticate_member(host, form_data, db)
    # access_token = generate_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
