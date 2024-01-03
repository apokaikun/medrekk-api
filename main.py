from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uvicorn
from medrekk.database.connection import create_db_and_tables, get_db
from medrekk.schemas.token import Token
from medrekk.controllers import authenticate_user
from medrekk.utils.auth import generate_access_token
from medrekk.routes import user_routes

app = FastAPI()

app.include_router(user_routes)


@app.get('/')
async def root() -> dict:
    create_db_and_tables()
    return {'message': 'Welcome to MedRekk API!'}


@app.get('/drop')
async def drop(
    db: Session = Depends(get_db)
):
    create_db_and_tables(True)
    return {}


@app.post('/auth', response_model=Token)
def login(
    user_form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db, user_form_data)
    access_token = generate_access_token(user[0])
    return {'access_token': access_token, 'token_type': 'bearer'}


if __name__ == "__main__":
    uvicorn.run(app)
