import hmac
import re
from datetime import datetime, timedelta
from typing import Annotated, Optional

import bcrypt
import shortuuid
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from jose.constants import ALGORITHMS

from medrekk.database.token import token_store
from medrekk.dependencies import oauth2_scheme
from medrekk.schemas.accounts import MemberRead
from medrekk.schemas.token import Token
from medrekk.models.medrekk import MedRekkAccount
from .constants import HMAC_KEY, JWT_KEY, TOKEN_EXPIRE_MINUTES


def generate_access_token(member: MemberRead, account: Optional[MedRekkAccount] = None) -> Token:
    
    account_id = account.id if account else member.account_id


    iat = datetime.now()
    exp = iat + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    sub = f"{member.id},{account_id}"
    jti = shortuuid.uuid()
    claims = {"sub": sub, "iat": iat, "exp": exp, "jti": jti}
    to_join = [str(i) for i in claims.values()]

    aud = hmac.new(
        HMAC_KEY.encode(), ".".join(sorted(to_join)).encode(), "SHA256"
    ).hexdigest()

    claims["aud"] = aud

    token_store.set_token(jti=jti, aud=aud)

    token = jwt.encode(claims, JWT_KEY, algorithm=ALGORITHMS.HS256)

    return token


def verify_jwt_token(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    unverified = jwt.get_unverified_claims(token)
    jti = unverified["jti"]
    aud = token_store.get_token(jti=jti)

    try:
        return jwt.decode(token, JWT_KEY, algorithms=ALGORITHMS.HS256, audience=aud)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token.",
        )


def get_member_id(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    unverified = jwt.get_unverified_claims(token)
    sub: str = unverified["sub"]
    member_id = sub.split(",")[0]
    return member_id


def get_account_id(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    unverified = jwt.get_unverified_claims(token)
    sub: str = unverified["sub"]
    account_id = sub.split(",")[1]
    return account_id


def check_self(token: Annotated[str, Depends(oauth2_scheme)], member_id: str):
    unverified = jwt.get_unverified_claims(token)
    sub = unverified.get("sub")
    if sub != member_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized."
        )
    return sub == member_id


def validate_password_strength(password):
    # Check if the password has at least 8 characters
    if len(password) < 8:
        return False

    # Check if the password contains at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # Check if the password contains at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # Check if the password contains at least one digit
    if not re.search(r"\d", password):
        return False

    # Check if the password contains at least one special character
    # r"[!@#$%^&*()_+{}\[\]:;\"'<>?,./\\|`~]"
    # r"[!@#$%^&*()\-_[\]{};':\",./<>?]"
    if not re.search(r"[!@#$%^&*()_+{}\[\]:;\"'<>?,./\\|`~]", password):
        return False

    # If all the conditions are met, the password is valid
    return True


# Add checking of password strength
def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt).decode()
    return hashed


def verify_password(hashed: str, input: str):
    # Check if the input password matches the hashed password
    return bcrypt.checkpw(input.encode("utf-8"), hashed.encode())
