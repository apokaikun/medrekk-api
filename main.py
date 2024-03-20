from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from medrekk.controllers.users import authenticate_user
from medrekk.database.connection import get_db
from medrekk.routes import *
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.schemas.token import Token
from medrekk.utils.auth import generate_access_token

VERSION = "0.0.1"
VERSION_SUFFIX = "pre-alpha"
DOCS_URL = "/latest/docs"
medrekk_app = FastAPI(
    title="MedRekk",
    version=f"version {VERSION}-{VERSION_SUFFIX}",
    docs_url=DOCS_URL,
    root_path=f"/v{VERSION}",
    debug=True,
)


@medrekk_app.get("/")
def root():
    # Redirects to docs URL for easier testing.
    return RedirectResponse(url=DOCS_URL)


@medrekk_app.post(
    "/latest/auth",
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
    user_form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = authenticate_user(db, user_form_data)
    access_token = generate_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


medrekk_app.include_router(user_routes)
medrekk_app.include_router(user_routes_verified)
medrekk_app.include_router(account_routes)
medrekk_app.include_router(profile_routes)
