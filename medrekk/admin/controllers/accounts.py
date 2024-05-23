from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from medrekk.admin.controllers.users import add_account_user
from medrekk.admin.schemas.accounts import AccountCreate, AccountRead, UserCreate
from medrekk.common.models import MedRekkAccount
from medrekk.common.models.medrekk import MedRekkUser
from medrekk.common.utils import shortid


def create_account(
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
        id=shortid(),
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    user_create = UserCreate(username=account.user_name, password=account.password)

    new_user = add_account_user(new_account.id, user_create, db)

    new_account.owner_id = new_user.id
    new_account.users.append(new_user)

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


def read_account(account_id: str, user_id: str, db: Session):
    account = db.get(MedRekkAccount, account_id)
    if account.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "content": {
                    "msg": "HTTP_401_UNAUTHORIZED. You are not authorized to read this account.",
                    "loc": "account_id",
                },
            },
        )

    return account


def read_account_from_host(host: str, user_id, db: Session):
    return (
        db.query(MedRekkAccount)
        .filter(MedRekkAccount.account_subdomain == host.split(".")[0])
        .filter(MedRekkAccount.users.any(MedRekkUser.id == user_id))
    )
