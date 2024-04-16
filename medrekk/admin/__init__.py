from fastapi import FastAPI
from medrekk.admin.routes.accounts import account_routes, account_routes_verified
from medrekk.admin.routes.users import user_routes
from medrekk.admin.routes.auth import auth_routes

VERSION = "202404"
VERSION_SUFFIX = "pre-alpha"
DOCS_URL = f"/{VERSION}-{VERSION_SUFFIX}/docs"

admin_app = FastAPI(
    title="MedRekk Admin",
    debug=True,
)

admin_app.include_router(auth_routes)

admin_app.include_router(account_routes)
admin_app.include_router(account_routes_verified)

admin_app.include_router(user_routes)