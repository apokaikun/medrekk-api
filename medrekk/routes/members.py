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
<<<<<<< HEAD
from medrekk.utils.auth import check_self, verify_jwt_token

member_routes_verified = APIRouter(
    prefix=f"/{routes.ACCOUNTS}", dependencies=[Depends(verify_jwt_token)]
)


@member_routes_verified.post(
    "/{account_id}/members/",
    response_model=UserRead,
=======
from medrekk.utils.auth import check_self, get_account_id, verify_jwt_token

member_routes = APIRouter(
    prefix=f"/{routes.MEMBERS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Account Members"],
)


@member_routes.post(
    "/",
    response_model=MemberRead,
>>>>>>> 25c02d6 (refactor)
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
<<<<<<< HEAD
    account_id: str,
    member_data: UserCreate,
=======
    account_id: Annotated[str, Depends(get_account_id)],
    member_data: MemberCreate,
>>>>>>> 25c02d6 (refactor)
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


<<<<<<< HEAD
@member_routes_verified.get(
    "/{account_id}/members/",
    response_model=List[UserListItem],
)
async def get_members(
    account_id: str,
=======
@member_routes.get(
    "/",
    response_model=List[MemberListItem],
)
async def get_members(
    account_id: Annotated[str, Depends(get_account_id)],
>>>>>>> 25c02d6 (refactor)
    db: Annotated[Session, Depends(get_db)],
):
    """
    Get all users.
    """
<<<<<<< HEAD
    users = read_users(account_id, db)
=======
    users = read_members(account_id, db)
>>>>>>> 25c02d6 (refactor)

    return [MemberListItem.model_validate(user) for user in users]


# Get a specific user by user ID
<<<<<<< HEAD
@member_routes_verified.get(
    "/{account_id}/members/{member_id}",
    response_model=UserRead,
)
async def get_user(
    account_id: str,
    member_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = read_user(account_id, member_id, db)
=======
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
>>>>>>> 25c02d6 (refactor)

    return MemberRead.model_validate(user)


# Delete self. Only self can delete itself.
# TODO: Add a scope based authorization to add a 'delete user' scope to delete other than self.


<<<<<<< HEAD
@member_routes_verified.delete(
    "/{account_id}/members/{member_id}",
    response_model=UserRead,
    dependencies=[Depends(check_self)],
)
async def delete_user(
    account_id: str,
    member_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = read_user(account_id, member_id, db)
=======
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
>>>>>>> 25c02d6 (refactor)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user and return the deleted user
    db.delete(user)
    db.commit()
    return None
