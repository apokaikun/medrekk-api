from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, APIKeyHeader

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
token_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="login", tokenUrl="token")

api_key_scheme = APIKeyHeader(name="X-Api-Key")