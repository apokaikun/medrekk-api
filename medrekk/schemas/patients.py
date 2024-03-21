from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PatientBase(BaseModel):
    id: str
    created: datetime = datetime.now()
    updated: datetime = datetime.now()

    model_config = ConfigDict(
        from_attributes=True, validate_assignment=True, arbitrary_types_allowed=True
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


# Patient Vitals:
#   PatientBloodPressure,
#   PatientHeartRate,
#   PatientRespiratoryRate,
#   PatientBodyTemperature
class PatientBloodPressureCreate(BaseModel):
    patient_id: str
    systolic: int
    diastolic: int


class PatientBloodPressureRead(PatientBloodPressureCreate, PatientBase):
    pass


class PatientBloodPressureUpdate(PatientBloodPressureCreate):
    updated: datetime = datetime.now()


class PatientBloodPressureDelete(BaseModel):
    id: str


class PatientHeartRateCreate(BaseModel):
    patient_id: str
    hear_rate: int


class PatientHeartRateRead(PatientHeartRateCreate, PatientBase):
    pass


class PatientHeartRateUpdate(PatientBloodPressureCreate):
    updated: datetime = datetime.now()


class PatientHeartRateDelete(BaseModel):
    id: str


class PatientRespiratoryRateCreate(BaseModel):
    patient_id: str
    respiratory_rate: int


class PatientRespiratoryRateRead(PatientRespiratoryRateCreate, PatientBase):
    pass


class PatientRespiratoryRateUpdate(PatientRespiratoryRateCreate):
    updated: datetime = datetime.now()


class PatientRespiratoryRateDelete(BaseModel):
    id: str


class PatientBodyTemperatureCreate(BaseModel):
    patient_id: str
    body_temperature: float


class PatientBodyTemperatureRead(PatientBodyTemperatureCreate, PatientBase):
    pass


class PatientBodyTemperatureUpdate(PatientBodyTemperatureCreate):
    updated: datetime = datetime.now()


class PatientBodyTemperatureDelete(BaseModel):
    id: str


class PatientBodyWeightCreate(BaseModel):
    patient_id: str
    body_weight: float


class PatientBodyWeightRead(PatientBodyWeightCreate, PatientBase):
    pass


class PatientBodyWeightUpdate(PatientBodyWeightCreate):
    updated: datetime = datetime.now()


class PatientBodyWeightDelete(BaseModel):
    id: str


class PatientHeightCreate(BaseModel):
    patient_id: str
    height: float


class PatientHeightRead(PatientHeightCreate, PatientBase):
    pass


class PatientHeightUpdate(PatientHeightCreate):
    updated: datetime = datetime.now()


class PatientHeightDelete(BaseModel):
    id: str


class PatientBodyMassIndexCreate(BaseModel):
    patient_id: str
    bmi: float


class PatientBodyMassIndexRead(PatientBodyMassIndexCreate, PatientBase):
    pass


class PatientBodyMassIndexUpdate(PatientBodyMassIndexCreate):
    updated: datetime = datetime.now()


class PatientBodyMassIndexDelete(BaseModel):
    id: str

class PatientFamilyHistoryCreate(BaseModel):
    patient_id: str
    hypertension: bool = False
    t2dm: bool = False
    asthma: bool = False
    cancer: str = False
    others: List[str] = []

class PatientFamilyHistoryRead(PatientFamilyHistoryCreate, PatientBase):
    pass

class PatientFamilyHistoryUpdate(PatientFamilyHistoryCreate):
    updated: datetime = datetime.now()

class PatientFamilyHistoryDelete(BaseModel):
    id: str

class PatientHospitalizationHistoryCreate(BaseModel):
    patient_id: str
    chief_complaint: str
    admission_date: date
    discharge_date: date
    notes: str

class PatientHospitalizationHistoryRead(PatientHospitalizationHistoryCreate, PatientBase):
    pass

class PatientHospitalizationHistoryUpdate(PatientHospitalizationHistoryCreate):
    updated: datetime = datetime.now()

class PatientHospitalizationHistoryDelete(BaseModel):
    id: str

class PatientMedicalHistoryCreate(BaseModel):
    patient_id: str
    hypertension: bool = False
    t2dm: bool = False
    asthma: bool = False
    cancer: bool = False
    others: List[str] = []

class PatientMedicalHistoryRead(PatientMedicalHistoryCreate, PatientBase):
    pass

class PatientMedicalHistoryUpdate(PatientMedicalHistoryCreate):
    updated: datetime = datetime.now()

class PatientMedicalHistoryDelete(BaseModel):
    id: str

class PatientMedicationCreate(BaseModel):
    patient_id: str
    medication: str
    start_date: datetime
    end_date: Optional[datetime] = None
    notes: Optional[str] = None

class PatientMedicationRead(PatientMedicationCreate, PatientBase):
    pass

class PatientMedicationUpdate(PatientMedicationCreate):
    updated: datetime = datetime.now()

class PatientMedicationDelete(BaseModel):
    id: str

class PatientOBHistoryCreate(BaseModel):
    patient_id: str
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
    patient_id: str
    chief_complaint: str
    surgery_date: date
    notes: List[str] = []