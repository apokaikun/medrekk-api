from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from medrekk.controllers import create_user, read_user, read_users
from medrekk.database.connection import get_db
from medrekk.schemas import UserCreate, UserRead, UserListItem
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.utils.auth import check_self, verify_jwt_token

user_routes = APIRouter()


@user_routes.post(
    "/users/",
    response_model=UserRead,
    status_code=201,
    responses={
        409: {
            "description": "HTTP_409_CONFLICT. There is an error in creating the user.",
            "model": HTTP_EXCEPTION
        },
        500: {
            "description": "HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            "model": HTTP_EXCEPTION
        },
    },
)
async def register(
    user_form_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Create a new user. Requires `email` and `password`
    """
    user = create_user(user_form_data, db)
    if user is None:
        raise JSONResponse(
            content="HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            status_code=500,
            )
    return user


"""
Routes that requires a valid jwt_token
"""
user_routes_verified = APIRouter(dependencies=[Depends(verify_jwt_token)])


@user_routes_verified.get("/users/", response_model=List[UserListItem])
async def get_users(db: Annotated[Session, Depends(get_db)]):
    """
    Get all users.
    """
    return read_users(db)


# Get a specific user by user ID
@user_routes_verified.get(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(verify_jwt_token)],
)
async def get_user(
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return read_user(user_id, db)


# Delete self. Only self can delete itself.
# TODO: Add a scope based authorization to add a 'delete user' scope to delete other than self.


@user_routes_verified.delete(
    "/users/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(verify_jwt_token), Depends(check_self)],
)
async def delete_user(
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    user = read_user(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user and return the deleted user
    db.delete(user)
    db.commit()
    return user
