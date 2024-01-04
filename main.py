from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from medrekk.database.connection import get_db
from medrekk.schemas import Token
from medrekk.controllers import authenticate_user
from medrekk.utils.auth import generate_access_token
from medrekk.routes import user_routes, profile_routes
import uvicorn

app = FastAPI()

app.include_router(user_routes)
app.include_router(profile_routes)


@app.get('/')
async def root() -> dict:
    return {'message': 'Welcome to MedRekk API!'}


@app.post('/auth', response_model=Token)
def auth(
    user_form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = authenticate_user(db, user_form_data)
    access_token = generate_access_token(user[0])
    return {'access_token': access_token, 'token_type': 'bearer'}


# @app.get('/drop')
# async def drop(
#     db: Session = Depends(get_db)
# ):
#     create_db_and_tables(True)
#     return {}


if __name__ == "__main__":
    uvicorn.run(app)
