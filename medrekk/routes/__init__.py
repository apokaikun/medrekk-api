from .accounts import account_routes
from .patients import patient_routes
from .profiles import profile_routes
from .users import user_routes, user_routes_verified

__all__ = [
    "user_routes",
    "user_routes_verified",
    "account_routes",
    "profile_routes",
    "patient_routes",
]
