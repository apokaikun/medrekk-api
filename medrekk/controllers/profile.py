from sqlmodel import Session
from medrekk.models.profile import MedRekkProfile
from medrekk.schemas import ProfileCreate


def create_profile(
        profile: ProfileCreate,
        db: Session
):
    """
    Controller to handle user profile create requests.

    Parameters:
    """
    new_profile = MedRekkProfile().model_validate(profile)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile
