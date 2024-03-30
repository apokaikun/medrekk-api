from typing import List

from fastapi import HTTPException, status
<<<<<<< HEAD
from fastapi.security import OAuth2PasswordRequestForm
=======
from psycopg.errors import UniqueViolation
>>>>>>> 25c02d6 (refactor)
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

<<<<<<< HEAD
from medrekk.models import MedRekkUser
from medrekk.schemas import UserCreate, UserRead, UserUpdate
from medrekk.utils import shortid
from medrekk.utils.auth import hash_password, verify_password

from psycopg.errors import UniqueViolation

def authenticate_user(
    db: Session,
    user_form_data: OAuth2PasswordRequestForm,
) -> UserRead:
    user = read_member_by_username(db, user_form_data.username)
    
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


def add_account_member(
    user_form_data: UserCreate,
    db: Session,
) -> UserRead:
=======
from medrekk.models.medrekk import MedRekkMember
from medrekk.schemas.accounts import MemberCreate, MemberUpdate
from medrekk.utils import shortid
from medrekk.utils.auth import hash_password


def add_account_member(
    account_id: str,
    user_form_data: MemberCreate,
    db: Session,
) -> MedRekkMember:
>>>>>>> 25c02d6 (refactor)
    """
    Controller to handle user create requests.

    Parameters:

<<<<<<< HEAD
        user_create: UserCreate
=======
        user_create: MemberCreate
>>>>>>> 25c02d6 (refactor)
            object for the request.
        db: Session
            Database session
    """

    try:
        # Test if username provided is an email.
<<<<<<< HEAD
        # User pydantic's EmailStr data-type for validation.
        user = MedRekkUser(
            id=shortid(),
            username=user_form_data.username,
            password=hash_password(
                user_form_data.password.get_secret_value(),
            ),
        )
=======
        # Member pydantic's EmailStr data-type for validation.
        hashed_password = hash_password(user_form_data.password.get_secret_value())
        user = MedRekkMember(
            id=shortid(),
            username=user_form_data.username,
            password=hashed_password,
            account_id=account_id,
        )

>>>>>>> 25c02d6 (refactor)
        db.add(user)
        db.commit()
        db.refresh(user)

<<<<<<< HEAD
        return UserRead.model_validate(user)
=======
        return user
>>>>>>> 25c02d6 (refactor)
    except DBAPIError as e:
        # sqlstate = e.orig.sqlstate
        # if sqlstate == "23505":
        if isinstance(e.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
<<<<<<< HEAD
                        "msg": f"Username {user.username} is already used.",
=======
                        "msg": f"Membername {user.username} is already used.",
>>>>>>> 25c02d6 (refactor)
                        "loc": "username",
                    },
                },
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
<<<<<<< HEAD
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def read_member(user_id: int, db: Session) -> MedRekkUser:
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
        
        
=======
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )


def read_member(
    account_id: str,
    member_id: int,
    db: Session,
) -> MedRekkMember:
    try:
        user = (
            db.query(MedRekkMember)
            .filter(MedRekkMember.account_id == account_id)
            .filter(MedRekkMember.id == member_id)
            .one_or_none()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "content": {
                        "msg": f"Member is member_id:{member_id} does not exist.",
                        "loc": "member_id",
                    },
                },
            )

        return user

>>>>>>> 25c02d6 (refactor)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
<<<<<<< HEAD
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def read_member_by_username(db: Session, username: str) -> MedRekkUser:
    try:
        select_stmt = select(MedRekkUser).where(MedRekkUser.username == username)
        user = db.scalars(select_stmt).first()
        
        if user:
            return user
        
=======
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )


def read_member_by_username(
    username: str,
    db: Session,
) -> MedRekkMember:
    try:
        user = (
            db.query(MedRekkMember)
            .filter(MedRekkMember.username == username)
            .one_or_none()
        )

        if user:
            return user

>>>>>>> 25c02d6 (refactor)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
<<<<<<< HEAD
                    "msg": f"User `{username}` does not exist.",
=======
                    "msg": f"Member `{username}` does not exist.",
>>>>>>> 25c02d6 (refactor)
                    "loc": "username",
                },
            },
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
<<<<<<< HEAD
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def read_members(db: Session) -> List[MedRekkUser]:
    try:
        # select_stmt = select(MedRekkUser)
        # users = db.scalars(select_stmt).all()
        users = db.query(MedRekkUser).all()
=======
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )


def read_members(account_id: str, db: Session) -> List[MedRekkMember]:
    try:
        # select_stmt = select(MedRekkMember)
        # users = db.scalars(select_stmt).all()
        users = (
            db.query(MedRekkMember).filter(MedRekkMember.account_id == account_id).all()
        )
>>>>>>> 25c02d6 (refactor)
        return users
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
<<<<<<< HEAD
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )


def update_member(db: Session, user_id: int, user: UserUpdate):

    db_user = db.query(UserCreate).filter(UserCreate.id == user_id).first()
=======
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )


def update_member(db: Session, member_id: int, user: MemberUpdate):

    db_user = db.query(MemberCreate).filter(MemberCreate.id == member_id).first()
>>>>>>> 25c02d6 (refactor)
    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


<<<<<<< HEAD
def delete_member(db: Session, user_id: int):
    try:
        select_stmt = select(MedRekkUser).where(MedRekkUser.id == user_id)
=======
def delete_member(db: Session, member_id: int):
    try:
        select_stmt = select(MedRekkMember).where(MedRekkMember.id == member_id)
>>>>>>> 25c02d6 (refactor)
        db_user = db.scalars(select_stmt).first()
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
<<<<<<< HEAD
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
        )
=======
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )


__all__ = [
    "add_account_member",
    "read_member",
    "read_member_by_username",
    "read_members",
    "update_member",
    "delete_member",
]
>>>>>>> 25c02d6 (refactor)
