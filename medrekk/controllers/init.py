from medrekk.controllers.accounts import create_account, read_account
from medrekk.controllers.patients import create_patient
from medrekk.schemas.accounts import AccountCreate
from medrekk.schemas.patients import PatientProfileCreate
from sqlalchemy.orm import Session

from medrekk.utils import shortid

def init_db(db:Session):
    account = AccountCreate(
        account_name='awesome account',
        user_name='a@a.com',
        password='aaaa'
    )
    create_account(account, db)

    patient = PatientProfileCreate(
        lastname = "endres",
        middlename = "",
        firstname = "kai",
        suffix = "",
        birthdate = "1982-10-14",
        gender = "string",
        mobile = "string",
        email = "string",
        address_country = "Philippines",
        address_province = "string",
        address_city = "string",
        address_barangay = "string",
        address_line1 = "string",
        address_line2 = "",
        religion = "Roman Catholic"
    )

    create_patient(patient, db)