from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from medrekk.admin.controllers.users import add_account_user, read_user, read_users
from medrekk.common.database.connection import get_db
from medrekk.admin.schemas.accounts import UserCreate, UserListItem, UserRead
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.common.utils import routes
from medrekk.common.utils.auth import check_self, get_account_id, verify_jwt_token

user_routes = APIRouter(
    prefix=f"/{routes.MEMBERS}",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Account Users"],
)


@user_routes.post(
    "/",
    response_model=UserRead,
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
async def add_user(
    account_id: Annotated[str, Depends(get_account_id)],
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Create a new user. Requires `email` and `password`

    This is a new line:
    --------------


    """
    user = add_account_user(account_id, user_data, db)
    if user is None:
        raise JSONResponse(
            content="HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            status_code=500,
        )
    return user


"""
Routes that requires a valid jwt_token
"""


@user_routes.get(
    "/",
    response_model=List[UserListItem],
)
async def get_users(
    account_id: Annotated[str, Depends(get_account_id)],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Get all users.
    """
    users = read_users(account_id, db)

    return [UserListItem.model_validate(user) for user in users]


# Get a specific user by user ID
@user_routes.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user(
    account_id: Annotated[str, Depends(get_account_id)],
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = read_user(account_id, user_id, db)

    return UserRead.model_validate(user)


# Delete self. Only self can delete itself.
# TODO: Add a scope based authorization to add a 'delete user' scope to delete other than self.


@user_routes.delete(
    "/{user_id}",
    dependencies=[Depends(check_self)],
)
async def delete_user(
    account_id: Annotated[str, Depends(get_account_id)],
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = read_user(account_id, user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user and return the deleted user
    db.delete(user)
    db.commit()
    return None
