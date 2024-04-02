from typing import List

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.models.medrekk import MedRekkMember
from medrekk.schemas.accounts import MemberCreate, MemberUpdate
from medrekk.utils import shortid
from medrekk.utils.auth import hash_password


def add_account_member(
    account_id: str,
    user_form_data: MemberCreate,
    db: Session,
) -> MedRekkMember:
    """
    Controller to handle user create requests.

    Parameters:

        user_create: MemberCreate
            object for the request.
        db: Session
            Database session
    """

    try:
        # Test if username provided is an email.
        # Member pydantic's EmailStr data-type for validation.
        hashed_password = hash_password(user_form_data.password.get_secret_value())
        user = MedRekkMember(
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
                        "msg": f"Membername {user.username} is already used.",
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

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "msg": f"Member `{username}` does not exist.",
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


def read_members(account_id: str, db: Session) -> List[MedRekkMember]:
    try:
        # select_stmt = select(MedRekkMember)
        # users = db.scalars(select_stmt).all()
        users = (
            db.query(MedRekkMember).filter(MedRekkMember.account_id == account_id).all()
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


def update_member(db: Session, member_id: int, user: MemberUpdate):

    db_user = db.query(MemberCreate).filter(MemberCreate.id == member_id).first()
    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_member(db: Session, member_id: int):
    try:
        select_stmt = select(MedRekkMember).where(MedRekkMember.id == member_id)
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
    "add_account_member",
    "read_member",
    "read_member_by_username",
    "read_members",
    "update_member",
    "delete_member",
]
