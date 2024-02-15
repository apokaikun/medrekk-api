from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from medrekk.database.connection import get_db
# from medrekk.schemas.accounts import AccountCreate

from medrekk.utils.auth import verify_jwt_token


account_routes = APIRouter(prefix='/account', dependencies=[
                           Depends(verify_jwt_token)])


# @account_routes.post('')
# def create_account(
#     account: AccountCreate,
#     db: Annotated[Session, Depends(get_db)]
# ):
#     pass
