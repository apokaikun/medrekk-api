from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PatientBase(BaseModel):
    id: str
    created: datetime = datetime.now()
    updated: datetime = datetime.now()

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )


# Patient profile
class PatientProfileCreate(BaseModel):
    lastname: str = Field(title="Patient Lastname")
    middlename: Optional[str] = ""
    firstname: str
    suffix: Optional[str] = ""
    birthdate: date
    gender: str
    mobile: Optional[str] = None
    email: Optional[str] = None
    address_country: str = "Philippines"
    address_province: str
    address_city: str
    address_barangay: str
    address_line1: str
    address_line2: Optional[str] = ""
    religion: str = "Roman Catholic"


class PatientProfileRead(PatientProfileCreate, PatientBase):
    url: str = ""
    pass


class PatientProfileUpdate(PatientProfileCreate):
    updated: datetime = datetime.now()


class PatientProfileDelete(BaseModel):
    id: str


class PatientBloodPressureCreate(BaseModel):
    dt_measured: datetime
    systolic: int
    diastolic: int


class PatientBloodPressureRead(PatientBloodPressureCreate, PatientBase):
    pass


class PatientBloodPressureUpdate(PatientBloodPressureCreate):
    updated: datetime = datetime.now()


class PatientBloodPressureDelete(BaseModel):
    id: str


class PatientHeartRateCreate(BaseModel):
    dt_measured: datetime
    heart_rate: int


class PatientHeartRateRead(PatientHeartRateCreate, PatientBase):
    pass


class PatientHeartRateUpdate(PatientHeartRateCreate):
    updated: datetime = datetime.now()


class PatientHeartRateDelete(BaseModel):
    id: str


class PatientRespiratoryRateCreate(BaseModel):
    dt_measured: datetime
    respiratory_rate: int


class PatientRespiratoryRateRead(PatientRespiratoryRateCreate, PatientBase):
    pass


class PatientRespiratoryRateUpdate(PatientRespiratoryRateCreate):
    updated: datetime = datetime.now()


class PatientRespiratoryRateDelete(BaseModel):
    id: str


class PatientBodyTemperatureCreate(BaseModel):
    dt_measured: datetime
    body_temperature: float


class PatientBodyTemperatureRead(PatientBodyTemperatureCreate, PatientBase):
    pass


class PatientBodyTemperatureUpdate(PatientBodyTemperatureCreate):
    updated: datetime = datetime.now()


class PatientBodyTemperatureDelete(BaseModel):
    id: str


class PatientBodyWeightCreate(BaseModel):
    date_measured: date
    body_weight: float


class PatientBodyWeightRead(PatientBodyWeightCreate, PatientBase):
    pass


class PatientBodyWeightUpdate(PatientBodyWeightCreate):
    updated: datetime = datetime.now()


class PatientBodyWeightDelete(BaseModel):
    id: str


class PatientHeightCreate(BaseModel):
    date_measured: date
    height: float


class PatientHeightRead(PatientHeightCreate, PatientBase):
    pass


class PatientHeightUpdate(PatientHeightCreate):
    updated: datetime = datetime.now()


class PatientHeightDelete(BaseModel):
    id: str


class PatientBodyMassIndexCreate(BaseModel):
    date_measured: date
    bmi: float


class PatientBodyMassIndexRead(PatientBodyMassIndexCreate, PatientBase):
    pass


class PatientBodyMassIndexUpdate(PatientBodyMassIndexCreate):
    updated: datetime = datetime.now()


class PatientBodyMassIndexDelete(BaseModel):
    id: str


class PatientFamilyHistoryCreate(BaseModel):
    hypertension: bool = False
    t2dm: bool = False
    asthma: bool = False
    cancer: bool = False
    others: List[str] = []
    notes: List[str] = []


class PatientFamilyHistoryRead(PatientFamilyHistoryCreate, PatientBase):
    pass


class PatientFamilyHistoryUpdate(PatientFamilyHistoryCreate):
    updated: datetime = datetime.now()


class PatientFamilyHistoryDelete(BaseModel):
    id: str


class PatientHospitalizationHistoryCreate(BaseModel):
    chief_complaint: str
    admission_date: date
    discharge_date: date
    notes: str


class PatientHospitalizationHistoryRead(
    PatientHospitalizationHistoryCreate, PatientBase
):
    pass


class PatientHospitalizationHistoryUpdate(PatientHospitalizationHistoryCreate):
    updated: datetime = datetime.now()


class PatientHospitalizationHistoryDelete(BaseModel):
    id: str


class PatientMedicalHistoryCreate(BaseModel):
    hypertension: bool = False
    t2dm: bool = False
    asthma: bool = False
    cancer: bool = False
    others: List[str] = []
    notes: List[str] = []


class PatientMedicalHistoryRead(PatientMedicalHistoryCreate, PatientBase):
    pass


class PatientMedicalHistoryUpdate(PatientMedicalHistoryCreate):
    updated: datetime = datetime.now()


class PatientMedicalHistoryDelete(BaseModel):
    id: str


class PatientMedicationCreate(BaseModel):
    medication: str
    start_date: datetime
    end_date: Optional[datetime] = None
    notes: List[str] = []


class PatientMedicationRead(PatientMedicationCreate, PatientBase):
    pass


class PatientMedicationUpdate(PatientMedicationCreate):
    updated: datetime = datetime.now()


class PatientMedicationDelete(BaseModel):
    id: str


class PatientOBHistoryCreate(BaseModel):
    gravida: int
    para: int
    term: int
    abortion: int
    living: int
    lmp: Optional[date] = None
    others: List[str] = []
    notes: List[str] = []


class PatientOBHistoryRead(PatientOBHistoryCreate, PatientBase):
    pass


class PatientOBHistoryUpdate(PatientOBHistoryCreate):
    updated: datetime = datetime.now()


class PatientOBHistoryDelete(BaseModel):
    id: str


class PatientSurgicalHistoryCreate(BaseModel):
    chief_complaint: str
    surgery_date: date
    notes: List[str] = []


class PatientSurgicalHistoryRead(PatientSurgicalHistoryCreate, PatientBase):
    pass


class PatientSurgicalHistoryUpdate(PatientSurgicalHistoryCreate):
    pass


class PatientAllergyCreate(BaseModel):
    """
    class PatientAllergyCreate(BaseModel):
        allergen: str
        reaction_description: str
    """

    allergen: str
    reaction_description: str
    notes: List[str] = []


class PatientAllergyRead(PatientAllergyCreate, PatientBase):
    pass


class PatientAllergyUpdate(PatientAllergyCreate):
    pass


class PatientImmunizationCreate(BaseModel):
    """
    class PatientImmunizationCreate(BaseModel):
        allergen: str
        reaction_description: str
    """

    vaccine: str
    date_administered: str
    notes: List[str] = []


class PatientImmunizationRead(PatientImmunizationCreate, PatientBase):
    pass


class PatientImmunizationUpdate(PatientImmunizationCreate):
    pass
