from fastapi import HTTPException, status
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from medrekk.models import MedRekkUserProfile
from medrekk.schemas import ProfileCreate, ProfileRead


def create_profile(
    profile: ProfileCreate,
    user_id: str,
    db: Session,
) -> ProfileRead:
    try:
        new_profile = MedRekkUserProfile(**profile.model_dump())
        new_profile.user_id = user_id

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
    except DBAPIError as e:
        sqlstate = e.orig.sqlstate
        if sqlstate == "23505":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "status_code": status.HTTP_409_CONFLICT,
                    "content": {
                        "msg": f"Profile for {user_id} already exists.",
                        "loc": "user_id",
                    },
                },
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "msg": "The server encountered an unexpected condition that prevented it from fulfilling the request. If the error occurs after several retries, please contact the administrator at: ...",
                },
            },
        )
    validated = ProfileRead.model_validate(new_profile)

    return validated


def read_profile(
    profile_id: str,
    user_id: str,
    db: Session,
) -> ProfileRead:
    profile = db.get(MedRekkUserProfile, profile_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {"msg": f"Profile with id: `{profile_id}` does not exist."},
            },
        )
    # Add this as a dependency. `own_profile`
    if profile and profile.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "content": {
                    "msg": f"You do not have enough privileges to read profile with id: {profile_id}",
                },
            },
        )

    return ProfileRead.model_validate(profile)
