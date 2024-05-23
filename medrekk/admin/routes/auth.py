from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from medrekk.admin.controllers.auth import authenticate_user
from medrekk.common.database.connection import get_session
from medrekk.common.utils.auth import get_host
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.admin.schemas.token import Token

auth_routes = APIRouter(tags=["Authentication"])


@auth_routes.post(
    "/auth",
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
    host: Annotated[str, Depends(get_host)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: Annotated[Session, Depends(get_session)],
) -> Token:
    access_token = authenticate_user(host, form_data, db_session)

    return JSONResponse(
        headers={"WWW-Authenticate": f"Bearer {access_token}"},
        content={"access_token": access_token, "token_type": "bearer"},
    )
