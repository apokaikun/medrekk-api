from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from medrekk.models import MedRekkAccount, MedRekkUser
from medrekk.schemas import AccountCreate, AccountRead


def create_account(
    account: AccountCreate,
    user_id: str,
    db: Session,
) -> AccountRead:
    try:
        # Check if accountname is unique. Lowercase comparison.
        duplicate = (
            db.query(MedRekkAccount)
            .filter(
                func.lower(MedRekkAccount.account_name) == account.account_name.lower()
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
            account_name=account.account_name,
            owner_id=user_id,
        )

        user = db.get(MedRekkUser, user_id)

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

        # Add self as member of the account
        new_account.members.append(user)
        db.commit()
        db.refresh(new_account)

        return AccountRead.model_validate(new_account)

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


def read_accounts(user_id: str, db: Session):
    try:
        stmt = select(MedRekkAccount).where(MedRekkAccount.owner_id == user_id)
        accounts = db.scalars(statement=stmt).all()

        validated_accounts = []
        for account in accounts:
            validated_accounts.append(AccountRead.model_validate(account))

        return validated_accounts
    
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


def read_account(account_id: str, user_id: str, db: Session):
    account = db.get(MedRekkAccount, account_id)
    if account.owner.id != user_id:
        raise HTTPException(400)

    return account
