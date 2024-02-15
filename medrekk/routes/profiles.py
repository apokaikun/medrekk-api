# from typing import Annotated
# from fastapi import APIRouter, Depends
# from sqlmodel import Session
# from medrekk.database.connection import get_db
# from medrekk.controllers import create_profile, read_profile
# from medrekk.schemas import ProfileCreate, ProfileRead
# from medrekk.utils.auth import verify_jwt_token


# profile_routes = APIRouter(
#     prefix="/patient", dependencies=[Depends(verify_jwt_token)])


# @profile_routes.post("/profiles/", response_model=ProfileRead)
# def create_profile(
#     profile: ProfileCreate,
#     db: Annotated[Session, Depends(get_db)]
# ):
#     new_profile = create_profile(profile, db)
#     return new_profile


# @profile_routes.get("/profiles/{profile_id}")
# def get_profile(
#     profile_id: str,
#     db: Annotated[Session, Depends(get_db)]
# ):
#     profile = read_profile(profile_id, )
