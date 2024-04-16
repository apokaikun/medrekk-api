from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from medrekk.admin.routes.accounts import account_routes, account_routes_verified
from medrekk.admin.routes.users import user_routes
from medrekk.admin.routes.auth import auth_routes
from medrekk.common.database.connection import get_db
from medrekk.common.controllers.init import init_db
from medrekk.patient.routes import (
    allergy_routes,
    bloodpressure_routes,
    bmi_routes,
    bodyheight_routes,
    bodytemp_routes,
    bodyweight_routes,
    diagnosis_routes,
    family_history_routes,
    heartrate_routes,
    hospitalization_history_routes,
    immunization_routes,
    medical_history_routes,
    medication_routes,
    ob_history_routes,
    patient_routes,
    record_routes,
    respiratory_routes,
    surgical_history_routes,
)

VERSION = "202403"
VERSION_SUFFIX = "pre-alpha"
DOCS_URL = f"/{VERSION}-{VERSION_SUFFIX}/docs"

medrekk_app = FastAPI(
    title="MedRekk",
    version=f"{VERSION}-{VERSION_SUFFIX}",
    docs_url=DOCS_URL,
    root_path=f"/api/{VERSION}-{VERSION_SUFFIX}",
    debug=True,
)


@medrekk_app.get("/")
def root():
    # Redirects to docs URL for easier testing.
    return RedirectResponse(url=DOCS_URL)


@medrekk_app.get("/init")
def root(init: bool, db: Annotated[Session, Depends(get_db)]):
    if init:
        init_db(db)
    return RedirectResponse(url=DOCS_URL)


medrekk_app.include_router(auth_routes)

medrekk_app.include_router(account_routes)
medrekk_app.include_router(account_routes_verified)
medrekk_app.include_router(user_routes)

medrekk_app.include_router(patient_routes)
medrekk_app.include_router(bodyweight_routes)
medrekk_app.include_router(bodyheight_routes)
medrekk_app.include_router(bmi_routes)

medrekk_app.include_router(family_history_routes)
medrekk_app.include_router(medical_history_routes)
medrekk_app.include_router(ob_history_routes)

medrekk_app.include_router(hospitalization_history_routes)
medrekk_app.include_router(surgical_history_routes)
medrekk_app.include_router(medication_routes)
medrekk_app.include_router(allergy_routes)
medrekk_app.include_router(immunization_routes)

medrekk_app.include_router(record_routes)
medrekk_app.include_router(diagnosis_routes)
# lab results
medrekk_app.include_router(bloodpressure_routes)
medrekk_app.include_router(heartrate_routes)
medrekk_app.include_router(respiratory_routes)
medrekk_app.include_router(bodytemp_routes)
