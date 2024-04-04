from typing import Annotated

from fastapi import Depends, FastAPI, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from medrekk.controllers.init import init_db
from medrekk.database.connection import get_db
from medrekk.routes.auth import auth_routes
from medrekk.routes.patient_bloodpressures import bloodpressure_routes
from medrekk.routes.patient_heartrates import heartrate_routes
from medrekk.routes.patient_record import record_routes
from medrekk.routes.patients import patient_routes
from medrekk.routes.patient_respiratory import respiratory_routes
from medrekk.routes.patient_temperature import bodytemp_routes
from medrekk.routes.patient_weight import bodyweight_routes
from medrekk.routes.patient_height import bodyheight_routes
from medrekk.routes.patient_bmi import bmi_routes
from medrekk.routes.patient_family_history import family_history_routes

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
# medrekk_app.include_router(account_routes)
# medrekk_app.include_router(account_routes_verified)
# medrekk_app.include_router(member_routes)
medrekk_app.include_router(patient_routes)
medrekk_app.include_router(record_routes)
medrekk_app.include_router(bloodpressure_routes)
medrekk_app.include_router(heartrate_routes)
medrekk_app.include_router(respiratory_routes)
medrekk_app.include_router(bodytemp_routes)
medrekk_app.include_router(bodyweight_routes)
medrekk_app.include_router(bodyheight_routes)
medrekk_app.include_router(bmi_routes)
medrekk_app.include_router(family_history_routes)
