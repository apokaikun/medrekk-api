from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from medrekk.controllers.users import authenticate_user
from medrekk.database.connection import get_db
from medrekk.routes.accounts import account_routes, account_routes_verified
from medrekk.routes.auth import auth_routes
from medrekk.routes.members import member_routes
# from medrekk.schemas.responses import HTTP_EXCEPTION
# from medrekk.schemas.token import Token
from medrekk.utils.auth import generate_access_token

VERSION = "202403"
VERSION_SUFFIX = "pre-alpha"
DOCS_URL = f"/{VERSION}-{VERSION_SUFFIX}/docs"

medrekk_app = FastAPI(
    title="MedRekk",
    version=f"{VERSION}-{VERSION_SUFFIX}",
    docs_url=DOCS_URL,
    root_path=f"/api/{VERSION}-{VERSION_SUFFIX}",
    debug=True,
)


@medrekk_app.get("/")
def root():
    # Redirects to docs URL for easier testing.
    return RedirectResponse(url=DOCS_URL)

medrekk_app.include_router(auth_routes)
medrekk_app.include_router(account_routes)
medrekk_app.include_router(account_routes_verified)
medrekk_app.include_router(member_routes)
