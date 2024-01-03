from fastapi import HTTPException, Depends, status
from typing import Annotated
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import medrekk.controllers as ctrl
from medrekk.schemas import User
from medrekk.database.connection import get_db
from medrekk.utils.auth import verify_jwt_token
from medrekk.dependencies import oauth2_scheme
from jose.exceptions import JWTError

user_routes = APIRouter()


# Create a new user
@user_routes.post("/register/", response_model=User)
async def register(
    user_form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = ctrl.create_user(user_form_data, db)
    if user is None:
        raise HTTPException(status_code=500)
    return user


# Get a specific user by user ID
@user_routes.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        verify_jwt_token(token)
        return ctrl.read_user(user_id, db)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token.",
        )


"""
# Get users
@user_routes.get("/users/", response_model=List(User))
async def get_users(db: Session = Depends(get_db)):
    return ctrl.read_users(db)

# Update a user's information
@user_routes.put("/users/{user_id}", response_model=User)
async def put_user(user_id: int, user: User):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user's information
    users_db[user_id] = user
    return user

# Delete a user by user ID
@user_routes.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    if user_id < 0 or user_id >= len(users_db):
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete the user and return the deleted user
    deleted_user = users_db.pop(user_id)
    return deleted_user
"""
