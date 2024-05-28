from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
api_key_scheme = APIKeyHeader(name="X-Api-Key")
