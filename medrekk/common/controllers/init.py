from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy import func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.admin.controllers.accounts import create_account
from medrekk.admin.controllers.users import add_account_user
from medrekk.admin.schemas.accounts import AccountCreate, AccountRead, UserCreate
from medrekk.common.models.medrekk import MedRekkAccount, MedRekkUser
from medrekk.common.utils import shortid
from medrekk.common.utils.auth import hash_password
from medrekk.mrs.controllers.profile import create_patient
from medrekk.mrs.schemas.patients import PatientProfileCreate


def init_add_account_user(
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
            id='22ORdh3HZHK',
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


def init_create_account(
    account: AccountCreate,
    db: Session,
) -> AccountRead:
    # split() removes extra spaces in between words.
    account_name = " ".join(account.account_name.split())

    # Check if accountname is unique. Lowercase comparison.
    duplicate = (
        db.query(MedRekkAccount)
        .filter(func.lower(MedRekkAccount.account_name) == account_name.lower())
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status_code": status.HTTP_409_CONFLICT,
                "content": {
                    "msg": f"HTTP_409_CONFLICT. Account name '{account.account_name}' is already taken.",
                    "loc": "account_name",
                },
            },
        )

    new_account = MedRekkAccount(
        account_name=account_name,
        account_subdomain="-".join(account_name.lower().split()),
        id='22ORdgJor4P',
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    user_create = UserCreate(username=account.user_name, password=account.password)

    new_user = init_add_account_user(new_account.id, user_create, db)

    new_account.owner_id = new_user.id
    new_account.users.append(new_user)

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


def init_db(db: Session):
    account = AccountCreate(
        account_name="awesome account", user_name="test@a.com", password="aaaa"
    )
    init_create_account(account, db)

    patient = PatientProfileCreate(
        lastname="endres",
        middlename="",
        firstname="kai",
        suffix="",
        birthdate="1982-10-14",
        gender="string",
        mobile="string",
        email="string",
        address_country="Philippines",
        address_province="string",
        address_city="string",
        address_barangay="string",
        address_line1="string",
        address_line2="",
        religion="Roman Catholic",
    )

    create_patient(patient, db)
