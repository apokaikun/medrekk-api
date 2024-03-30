from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from medrekk.controllers.members import add_account_member, read_member, read_members
from medrekk.database.connection import get_db
from medrekk.schemas.accounts import MemberCreate, MemberListItem, MemberRead
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.utils import routes
from medrekk.utils.auth import check_self, get_account_id, verify_jwt_token

member_routes = APIRouter(
    prefix=f"/{routes.MEMBERS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Account Members"],
)


@member_routes.post(
    "/",
    response_model=MemberRead,
    status_code=201,
    responses={
        409: {
            "description": "HTTP_409_CONFLICT. There is an error in creating the user.",
            "model": HTTP_EXCEPTION,
        },
        500: {
            "description": "HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            "model": HTTP_EXCEPTION,
        },
    },
)
async def add_member(
    account_id: Annotated[str, Depends(get_account_id)],
    member_data: MemberCreate,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Create a new user. Requires `email` and `password`

    This is a new line:
    --------------


    """
    user = add_account_member(account_id, member_data, db)
    if user is None:
        raise JSONResponse(
            content="HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            status_code=500,
        )
    return user


"""
Routes that requires a valid jwt_token
"""


@member_routes.get(
    "/",
    response_model=List[MemberListItem],
)
async def get_members(
    account_id: Annotated[str, Depends(get_account_id)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Get all users.
    """
    users = read_members(account_id, db)

    return [MemberListItem.model_validate(user) for user in users]


# Get a specific user by user ID
@member_routes.get(
    "/{member_id}",
    response_model=MemberRead,
)
async def get_user(
    account_id: Annotated[str, Depends(get_account_id)],
    member_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = read_member(account_id, member_id, db)

    return MemberRead.model_validate(user)


# Delete self. Only self can delete itself.
# TODO: Add a scope based authorization to add a 'delete user' scope to delete other than self.


@member_routes.delete(
    "/{member_id}",
    dependencies=[Depends(check_self)],
)
async def delete_user(
    account_id: Annotated[str, Depends(get_account_id)],
    member_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = read_member(account_id, member_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user and return the deleted user
    db.delete(user)
    db.commit()
    return None
