from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from medrekk.controllers import create_profile, read_profile
from medrekk.database.connection import get_db
from medrekk.schemas import ProfileCreate, ProfileRead
from medrekk.schemas.responses import HTTP_EXCEPTION
from medrekk.utils.auth import get_user_id, verify_jwt_token

profile_routes = APIRouter(
    prefix="/profile",
    dependencies=[Depends(verify_jwt_token)],
)


@profile_routes.post(
    "/",
    response_model=ProfileRead,
    status_code=201,
    responses={
        409: {
            "description": "HTTP_409_CONFLICT. There is an error in creating the user.",
            "model": HTTP_EXCEPTION
        },
        500: {
            "description": "HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            "model": HTTP_EXCEPTION
        },
    },
)
async def new_profile(
    profile: ProfileCreate,
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    new_profile = create_profile(profile, user_id, db)

    return new_profile


@profile_routes.get(
    "/{profile_id}",
    response_model=ProfileRead,
    responses={
        401: {
            "description": "HTTP_401_UNAUTHORIZED. You do not have enough privileges to read the profile with id: `profile_id`.",
            "model": HTTP_EXCEPTION
        },
        404: {
            "description": "HTTP_404_NOT_FOUND. Profile does not exist.",
            "model": HTTP_EXCEPTION
        },
        500: {
            "description": "HTTP_500_INTERNAL_SERVER_ERROR. The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
            "model": HTTP_EXCEPTION
        },
    },
)
async def get_profile(
    profile_id: str,
    user_id: Annotated[str, Depends(get_user_id)],
    db: Annotated[Session, Depends(get_db)],
):
    profile = read_profile(profile_id, user_id, db)

    profile_verified = ProfileRead.model_validate(profile)

    return profile_verified
