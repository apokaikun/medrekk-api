from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
token_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="login", tokenUrl="token")
