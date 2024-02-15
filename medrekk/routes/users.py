from fastapi import HTTPException, Depends
from typing import Annotated, List
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from medrekk.controllers import read_user, read_users, create_user
from medrekk.database.connection import get_db
from medrekk.models import MedRekkUserRead
from medrekk.utils.auth import check_self, verify_jwt_token

user_routes = APIRouter()


@user_routes.post("/users/", response_model=MedRekkUserRead)
async def register(
    user_form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Create a new user. Requires `email` and `password`
    """
    user = create_user(user_form_data, db)
    if user is None:
        raise HTTPException(status_code=500)
    return user


"""
Routes that requires a valid jwt_token
"""
user_routes_verified = APIRouter(dependencies=[Depends(verify_jwt_token)])


@user_routes_verified.get("/users/", response_model=List[MedRekkUserRead])
async def get_users(
        db: Annotated[Session, Depends(get_db)]
):
    """
    Get all users.
    """
    return read_users(db)

# Get a specific user by user ID


@user_routes_verified.get("/users/{user_id}", response_model=MedRekkUserRead, dependencies=[Depends(verify_jwt_token)])
async def get_user(
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    return read_user(user_id, db)


# Delete self. Only self can delete itself.
# TODO: Add a scope based authorization to add a 'delete user' scope to delete other than self.

@user_routes_verified.delete("/users/{user_id}",
                             response_model=MedRekkUserRead,
                             dependencies=[Depends(verify_jwt_token), Depends(check_self)])
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
