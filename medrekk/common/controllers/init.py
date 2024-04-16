from sqlalchemy.orm import Session

from medrekk.admin.controllers.accounts import create_account
from medrekk.mrs.controllers.profile import create_patient
from medrekk.admin.schemas.accounts import AccountCreate
from medrekk.mrs.schemas.patients import PatientProfileCreate


def init_db(db: Session):
    account = AccountCreate(
        account_name="awesome account", user_name="a@a.com", password="aaaa"
    )
    create_account(account, db)

    patient = PatientProfileCreate(
        lastname="endres",
        middlename="",
        firstname="kai",
        suffix="",
        birthdate="1982-10-14",
        gender="string",
        mobile="string",
        email="string",
        address_country="Philippines",
        address_province="string",
        address_city="string",
        address_barangay="string",
        address_line1="string",
        address_line2="",
        religion="Roman Catholic",
    )

    create_patient(patient, db)
