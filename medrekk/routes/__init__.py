from .accounts import account_routes, account_routes_verified
<<<<<<< HEAD
from .patients import patient_routes
from .profiles import profile_routes
from .members import member_routes_verified
from .patient_bodytemperature import bodytemperature_routes
__all__ = [
    "member_routes_verified",
    "account_routes",
    "account_routes_verified",
    "profile_routes",
    "patient_routes",
    "bodytemperature_routes",
]
=======
from .auth import auth_routes

__all__ = [
    "account_routes", 
    "account_routes_verified",
    "auth_routes",
]
>>>>>>> 25c02d6 (refactor)
