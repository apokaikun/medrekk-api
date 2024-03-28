from typing import List

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.models import MedRekkUser
from medrekk.schemas import UserCreate, UserRead, UserUpdate
from medrekk.utils import shortid
from medrekk.utils.auth import hash_password, verify_password

from psycopg.errors import UniqueViolation

def authenticate_user(
    db: Session,
    user_form_data: OAuth2PasswordRequestForm,
) -> UserRead:
    user = read_user_by_username(db, user_form_data.username)
    
    if not verify_password(user.password, user_form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                    "status_code": status.HTTP_401_UNAUTHORIZED,
                    "content": {
                        "msg": f"Invalid credentials for {user_form_data.username}.",
                        "loc": "[username, password]",
                    },
                },
            headers={"WWW-Authenticate": "Basic"},
        )
    return UserRead.model_validate(user)


def create_user(
    user_form_data: UserCreate,
    db: Session,
) -> UserRead:
    """
    Controller to handle user create requests.

    Parameters:

        user_create: UserCreate
            object for the request.
        db: Session
            Database session
    """

    try:
        # Test if username provided is an email.
        # User pydantic's EmailStr data-type for validation.
        user = MedRekkUser(
            id=shortid(),
            username=user_form_data.username,
            password=hash_password(
                user_form_data.password.get_secret_value(),
            ),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return UserRead.model_validate(user)
    except DBAPIError as e:
        # sqlstate = e.orig.sqlstate
        # if sqlstate == "23505":
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": f"Username {user.username} is already used.",
                        "loc": "username",
                    },
                },
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def read_user(user_id: int, db: Session) -> MedRekkUser:
    try:
        user = db.get(MedRekkUser, user_id)

        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"User is user_id:{user_id} does not exist.",
                    "loc": "user_id",
                },
            },
        )
        
        return user
        
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def read_user_by_username(db: Session, username: str) -> MedRekkUser:
    try:
        select_stmt = select(MedRekkUser).where(MedRekkUser.username == username)
        user = db.scalars(select_stmt).first()
        
        if user:
            return user
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"User `{username}` does not exist.",
                    "loc": "username",
                },
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def read_users(db: Session) -> List[MedRekkUser]:
    try:
        # select_stmt = select(MedRekkUser)
        # users = db.scalars(select_stmt).all()
        users = db.query(MedRekkUser).all()
        return users
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def update_user(db: Session, user_id: int, user: UserUpdate):

    db_user = db.query(UserCreate).filter(UserCreate.id == user_id).first()
    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    try:
        select_stmt = select(MedRekkUser).where(MedRekkUser.id == user_id)
        db_user = db.scalars(select_stmt).first()
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )
