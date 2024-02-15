from pydantic import ValidationError
from sqlmodel import Session
from medrekk.models import MedRekkAccountCreate, MedRekkAccountRead, MedRekkAccount


def create_account(
        account: MedRekkAccountCreate,
        db: Session
) -> MedRekkAccountRead:
    try:
        new_account = MedRekkAccount(**account.model_copy())
        print("Create new Account:")
        print(new_account.model_dump_json())
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account
    except ValidationError as e:
        print(f"Validation error: {e.json()}")
    return
