from sqlmodel import Session, select
from medrekk.models.patient_profile import MedRekkPatientProfile


# def create_profile(
#         profile: ProfileCreate,
#         db: Session
# ):
#     """
#     Controller to handle user profile create requests.

#     Parameters:
#     """
#     new_profile = MedRekkPatientProfile().model_validate(profile)
#     db.add(new_profile)
#     db.commit()
#     db.refresh(new_profile)
#     return new_profile


# def read_profile(
#         profile_id: str,
#         db: Session
# ):
#     select_stmt = select(MedRekkPatientProfile).where(
#         MedRekkPatientProfile.id == profile_id)
#     profile = db.exec(select_stmt).first()
