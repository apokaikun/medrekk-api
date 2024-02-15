from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
import shortuuid
from sqlmodel import Session, select
from medrekk.models import MedRekkUser, MedRekkUserRead, MedRekkUserBase

from medrekk.dependencies import pwd_context


def authenticate_user(
    db: Session,
    user_form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> MedRekkUserRead:
    user = read_user_by_username(db, user_form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exists.",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not pwd_context.verify(user_form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid credentials for {user_form_data.username}.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return MedRekkUserRead(**user.model_dump())


def create_user(
    user_form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session
):
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
        MedRekkUserBase(username=user_form_data.username)
    except ValidationError as e:
        print(e.json())
        # TODO: return the error to client if username is not an email.
        return
    if read_user_by_username(db, user_form_data.username):
        raise HTTPException(
            status_code=422,
            detail={"error": f"Email {user_form_data.username} is already used."},
        )

    password = pwd_context.hash(user_form_data.password)
    user = MedRekkUser(username=user_form_data.username)
    user.password = password
    user.id = shortuuid.uuid()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def read_user(
    user_id: int,
    db: Session
) -> MedRekkUser:
    try:
        select_stmt = select(MedRekkUser).where(MedRekkUser.id == user_id)
        user = db.exec(select_stmt).first()
        return user
    except Exception as e:
        print(e)
        pass


def read_user_by_username(
    db: Session,
    username: str
) -> MedRekkUser:
    try:
        select_stmt = select(MedRekkUser).where(
            MedRekkUser.username == username)
        user = db.exec(select_stmt).first()
        return user

    except Exception as e:
        print(e)
        return


def read_users(db: Session) -> list[MedRekkUser]:
    try:
        select_stmt = select(MedRekkUser)
        return db.exec(select_stmt).all()
    except Exception as e:
        print(e)
        return

# def update_user(db: Session, user_id: int, user: UserUpdate):
#     db_user = db.query(MedRekkUser).filter(MedRekkUser.id == user_id).first()
#     for field, value in user.model_dump(exclude_unset=True).items():
#         setattr(db_user, field, value)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


def delete_user(db: Session, user_id: int):
    try:
        select_stmt = select(MedRekkUser).where(MedRekkUser.id == user_id)
        db_user = db.exec(select_stmt).first()
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception as e:
        print(e)
        return
