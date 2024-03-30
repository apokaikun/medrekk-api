from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from medrekk.controllers.members import read_member_by_username
from medrekk.schemas.token import Token
from medrekk.utils.auth import generate_access_token, verify_password
from medrekk.controllers.accounts import read_account, read_account_from_host

def authenticate_member(
    host: str,
    form_data: OAuth2PasswordRequestForm,
    db: Session,
) -> Token:
    user = read_member_by_username(form_data.username, db)
    if host.startswith('medrekk.com'):
        account = read_account(user.account_id, user.id, db)
    else:
        account = read_account_from_host(host, db)
    access_token = generate_access_token(user, account)

    if not verify_password(user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "content": {
                    "msg": f"Invalid credentials for {form_data.username}.",
                    "loc": "[username, password]",
                },
            },
            headers={"WWW-Authenticate": "Basic"},
        )
    return access_token
