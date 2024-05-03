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
        raise e


def read_user(
    account_id: str,
    user_id: int,
    db: Session,
) -> MedRekkUser:
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
                    "msg": f"User with user_id:{user_id} does not exist.",
                    "loc": "user_id",
                },
            },
        )

    return user


def read_user_by_username(
    username: str,
    db: Session,
) -> MedRekkUser:
    user = db.query(MedRekkUser).filter(MedRekkUser.username == username).one_or_none()

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


def read_users(account_id: str, db: Session) -> List[MedRekkUser]:
    # select_stmt = select(MedRekkUser)
    # users = db.scalars(select_stmt).all()
    users = db.query(MedRekkUser).filter(MedRekkUser.account_id == account_id).all()
    return users


def update_user(account_id: str, user_id: str, user: UserUpdate, db: Session):
    db_user = read_user(account_id, user_id, db)

    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(account_id: str, user_id: str, db: Session):
    db_user = read_user(account_id, user_id, db)
    db.delete(db_user)
    db.commit()


__all__ = [
    "add_account_user",
    "read_user",
    "read_user_by_username",
    "read_users",
    "update_user",
    "delete_user",
]
