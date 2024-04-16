from datetime import timedelta
from redis import Redis

from medrekk.common.utils.constants import TOKEN_EXPIRE_MINUTES

token_db = Redis(host='localhost', port=6379, decode_responses=True, db=0)

class TokenStorage:
    def __init__(self, db: Redis) -> None:
        self.db: Redis = db

    def set_token(self, jti: str, aud: str) -> None:
        self.db.set(jti, aud, ex=timedelta(minutes=TOKEN_EXPIRE_MINUTES + 1))

    def get_token(self, jti: str) -> str | None:
        return self.db.get(jti)
    

token_store = TokenStorage(db=token_db)