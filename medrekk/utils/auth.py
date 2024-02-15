from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, Header, status
from medrekk.models import medrekk_user_account
from medrekk.schemas import Token
from medrekk.dependencies import oauth2_scheme
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from .constants import JWT_KEY, HMAC_KEY, jwts_
import shortuuid
import hmac


def generate_access_token(user: medrekk_user_account) -> Token:
    iat = datetime.now()
    exp = iat + timedelta(minutes=60)
    sub = user.id
    jti = shortuuid.uuid()
    claims = {"sub": sub, "iat": iat, "exp": exp, "jti": jti}
    to_join = [str(i) for i in claims.values()]

    aud = hmac.new(
        HMAC_KEY.encode(), ".".join(sorted(to_join)).encode(), "SHA256"
    ).hexdigest()

    claims["aud"] = aud

    jwts_[jti] = aud

    token = jwt.encode(claims, JWT_KEY, algorithm=ALGORITHMS.HS256)

    return token


def _verify_jwt_token(
    token: str,
) -> bool:
    pass


def verify_jwt_token(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> bool:
    unverified = jwt.get_unverified_claims(token)
    jti = unverified["jti"]
    aud = jwts_.get(jti)
    # If verification fails, jwterror is raised.
    try:
        return jwt.decode(token, JWT_KEY, algorithms=ALGORITHMS.HS256, audience=aud)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token.",
        )


def check_self(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_id: str
):
    unverified = jwt.get_unverified_claims(token)
    sub = unverified.get('sub')
    if sub != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized."
        )
    return sub == user_id
