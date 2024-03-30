from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from medrekk.routes.auth import auth_routes
from medrekk.routes.patient_bloodpressures import bloodpressure_routes
from medrekk.routes.patients import patient_routes

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


medrekk_app.include_router(auth_routes)
# medrekk_app.include_router(account_routes)
# medrekk_app.include_router(account_routes_verified)
# medrekk_app.include_router(member_routes)
medrekk_app.include_router(patient_routes)
medrekk_app.include_router(bloodpressure_routes)
