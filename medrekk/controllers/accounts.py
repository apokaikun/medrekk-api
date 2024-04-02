from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from medrekk.controllers.members import add_account_member
from medrekk.models import MedRekkAccount
from medrekk.schemas.accounts import AccountCreate, AccountRead, MemberCreate
from medrekk.utils import shortid


def create_account(
    account: AccountCreate,
    db: Session,
) -> AccountRead:
    try:
        # Check if accountname is unique. Lowercase comparison.
        account_name = " ".join(account.account_name.split())
        duplicate = (
            db.query(MedRekkAccount)
            .filter(
                func.lower(MedRekkAccount.account_name) == account_name.lower()
            )
            .first()
        )

        if duplicate:
            db.close()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": f"Account name '{account.account_name}' is already taken.",
                        "loc": "account_name",
                    },
                },
            )

        new_account = MedRekkAccount(
            account_name=account_name,
            account_subdomain="-".join(account_name.split()),
            id=shortid()
        )

        db.add(new_account)
        db.commit()
        db.refresh(new_account)

        member_create = MemberCreate(
            username=account.user_name, password=account.password
        )

        new_member = add_account_member(new_account.id, member_create, db)

        new_account.owner_id = new_member.id
        new_account.members.append(new_member)

        db.add(new_account)
        db.commit()
        db.refresh(new_account)

        if not new_account:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "content": {
                        "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                    },
                },
            )

        return new_account
    except HTTPException as e:
        raise e
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


def read_account(account_id: str, member_id: str, db: Session):
    account = db.get(MedRekkAccount, account_id)
    if account.owner_id != member_id:
        raise HTTPException(400)

    return account


def read_account_from_host(host: str, db: Session):
    return db.query(MedRekkAccount).filter(MedRekkAccount.account_subdomain == host.split(".")[0]).one_or_none()