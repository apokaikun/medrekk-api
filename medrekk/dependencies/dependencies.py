from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
token_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="login", tokenUrl="token")
