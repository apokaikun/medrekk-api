from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import ResponseValidationError
from sqlmodel import Session
from medrekk.database.connection import get_db
from medrekk.controllers import create_profile
from medrekk.schemas import ProfileCreate, Profile


profile_routes = APIRouter()


@profile_routes.post("/profiles/", response_model=Profile)
def new_profile(
    profile: ProfileCreate,
    db: Annotated[Session, Depends(get_db)]
):
    new_profile = create_profile(profile, db)
    return new_profile
