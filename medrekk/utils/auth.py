from datetime import datetime, timedelta
from fastapi import HTTPException, status
from medrekk.schemas import User, Token
from jose import jwt
from jose.constants import ALGORITHMS
from .constants import JWT_KEY, HMAC_KEY, jwts_
import shortuuid
import hmac


def generate_access_token(user: User) -> Token:
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


def verify_jwt_token(
    token: str,
) -> bool:
    unverified = jwt.get_unverified_claims(token)
    jti = unverified["jti"]
    aud = jwts_.get(jti)
    # If verification fails, jwterror is raised.
    return jwt.decode(token, JWT_KEY, algorithms=ALGORITHMS.HS256, audience=aud)