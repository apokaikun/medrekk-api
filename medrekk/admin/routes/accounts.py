from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import ValidationError
from sqlalchemy.orm import Session

from medrekk.admin.controllers.accounts import create_account, read_account
from medrekk.admin.schemas.accounts import AccountCreate, AccountRead
from medrekk.common.database.connection import get_db
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.common.utils import routes
from medrekk.common.utils.auth import get_account_id, get_user_id, verify_jwt_token

account_routes = APIRouter(
    prefix=f"/{routes.ACCOUNTS}",
    tags=["Accounts"],
    responses={
        500: {
            "description": "HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            "model": HTTP_EXCEPTION,
        },
    },
)


@account_routes.post(
    "/",
    name="Create New Account",
    response_model=AccountRead,
    status_code=201,
    responses={
        409: {
            "description": "HTTP_409_CONFLICT. There is an error in creating the account.",
            "model": HTTP_EXCEPTION,
        }
    },
)
async def new_account(
    account: AccountCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_account = create_account(account, db)
    return new_account


account_routes_verified = APIRouter(
    prefix=f"/{routes.ACCOUNTS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Accounts Verified"],
    responses={
        401: {
            "description": "This message indicates that you tried to access a resource that requires authorization, but your credentials (username/password OR token) were not recognized by the server.",
            "model": HTTP_EXCEPTION,
        }
    },
)


@account_routes_verified.get(
    "/",
    response_model=AccountRead,
)
async def get_account(
    account_id: Annotated[str, Depends(get_account_id)],
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    account = read_account(account_id, user_id, db)
    return account


@account_routes_verified.put("/", response_model=AccountRead)
async def set_account():
    pass
