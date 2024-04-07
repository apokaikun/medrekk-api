from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.common.models.medrekk import MedRekkUser
from medrekk.admin.schemas.accounts import UserCreate, UserUpdate
from medrekk.common.utils import shortid
from medrekk.common.utils.auth import hash_password


def add_account_user(
    account_id: str,
    user_form_data: UserCreate,
    db: Session,
) -> MedRekkUser:
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
        hashed_password = hash_password(user_form_data.password.get_secret_value())
        user = MedRekkUser(
            id=shortid(),
            username=user_form_data.username,
            password=hashed_password,
            account_id=account_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
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


def read_user(
    account_id: str,
    user_id: int,
    db: Session,
) -> MedRekkUser:
    try:
        user = (
            db.query(MedRekkUser)
            .filter(MedRekkUser.account_id == account_id)
            .filter(MedRekkUser.id == user_id)
            .one_or_none()
        )

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


def read_user_by_username(
    username: str,
    db: Session,
) -> MedRekkUser:
    try:
        user = (
            db.query(MedRekkUser)
            .filter(MedRekkUser.username == username)
            .one_or_none()
        )

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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )


def read_users(account_id: str, db: Session) -> List[MedRekkUser]:
    try:
        # select_stmt = select(MedRekkUser)
        # users = db.scalars(select_stmt).all()
        users = (
            db.query(MedRekkUser).filter(MedRekkUser.account_id == account_id).all()
        )
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


__all__ = [
    "add_account_user",
    "read_user",
    "read_user_by_username",
    "read_users",
    "update_user",
    "delete_user",
]
