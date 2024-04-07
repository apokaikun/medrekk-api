from .allergy import allergy_routes
from .bloodpressures import bloodpressure_routes
from .bmi import bmi_routes
from .body_temperature import bodytemp_routes
from .body_weight import bodyweight_routes
from .diagnosis import diagnosis_routes
from .family_history import family_history_routes
from .heart_rate import heartrate_routes
from .height import bodyheight_routes
from .hospitalization_history import hospitalization_history_routes
from .immunization import immunization_routes
from .medical_history import medical_history_routes
from .medication import medication_routes
from .ob_history import ob_history_routes
from .profile import patient_routes
from .record import record_routes
from .respiratory_rate import respiratory_routes
from .surgical_history import surgical_history_routes

__all__ = [
    "allergy_routes",
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
