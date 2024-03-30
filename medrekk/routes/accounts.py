from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from medrekk.controllers.accounts import create_account, read_account
from medrekk.database.connection import get_db
from medrekk.schemas.accounts import AccountCreate, AccountRead
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.utils import routes
from medrekk.utils.auth import get_account_id, get_member_id, verify_jwt_token

account_routes = APIRouter(
    prefix=f"/{routes.ACCOUNTS}",
    tags=["Accounts"],
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
        },
        500: {
            "description": "HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            "model": HTTP_EXCEPTION,
        },
    },
)
async def new_account(
    account: AccountCreate,
    db: Annotated[Session, Depends(get_db)],
):
    new_account = create_account(account, db)
    return AccountRead.model_validate(new_account)


account_routes_verified = APIRouter(
    prefix=f"/{routes.ACCOUNTS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Accounts Verified"],
)


@account_routes_verified.get(
    "/",
    response_model=AccountRead,
)
async def get_account(
    account_id: Annotated[str, Depends(get_account_id)],
    member_id: Annotated[str, Depends(get_member_id)],
    db: Annotated[Session, Depends(get_db)],
):
    account = read_account(account_id, member_id, db)
    return account


@account_routes_verified.put("/", response_model=AccountRead)
async def set_account():
    pass
