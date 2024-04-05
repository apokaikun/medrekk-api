from .accounts import account_routes, account_routes_verified

from .auth import auth_routes
from .patient_allergy import allergy_routes
from .patient_bloodpressures import bloodpressure_routes
from .patient_bmi import bmi_routes
from .patient_family_history import family_history_routes
from .patient_heartrates import heartrate_routes
from .patient_height import bodyheight_routes
from .patient_hospitalization_history import (
    hospitalization_history_routes,
)
from .patient_immunization import immunization_routes
from .patient_medical_history import medical_history_routes
from .patient_medication import medication_routes
from .patient_ob_history import ob_history_routes
from .patient_record import record_routes
from .patient_respiratory import respiratory_routes
from .patient_surgical_history import surgical_history_routes
from .patient_temperature import bodytemp_routes
from .patient_weight import bodyweight_routes
from .patients import patient_routes
from .patient_diagnosis import diagnosis_routes

__all__ = [
    "account_routes",
    "account_routes_verified",
    "allergy_routes",
    "auth_routes",
    "bloodpressure_routes",
    "bmi_routes",
    "bodyheight_routes",
    "bodytemp_routes",
    "bodyweight_routes",
    "diagnosis_routes",
    "family_history_routes",
    "heartrate_routes",
    "hospitalization_history_routes",
    "immunization_routes",
    "medical_history_routes",
    "medication_routes",
    "ob_history_routes",
    "patient_routes",
    "record_routes",
    "respiratory_routes",
    "surgical_history_routes",
]
