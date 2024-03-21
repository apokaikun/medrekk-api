from datetime import datetime

from sqlalchemy import (
    ARRAY,
    SMALLINT,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    String,
)

from medrekk.database.connection import Base
from medrekk.utils import shortid


class PatientBase:
    id = Column(String, default=shortid(), primary_key=True)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())


class PatientProfile(Base, PatientBase):
    __tablename__ = "patient_profile"

    lastname = Column(String, nullable=False)
    middlename = Column(String, nullable=True)
    firstname = Column(String, nullable=False)
    suffix = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address_country = Column(String, nullable=False)
    address_province = Column(String, nullable=False)
    address_city = Column(String, nullable=False)
    address_barangay = Column(String, nullable=False)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)
    religion = Column(String, nullable=False)


# Patient Vitals:
#   PatientBloodPressure,
#   PatientHeartRate,
#   PatientRespiratoryRate,
#   PatientBodyTemperature
class PatientBloodPressure(Base, PatientBase):
    __tablename__ = "patient_blood_pressure"

    patient_id = Column(ForeignKey("patient_profile.id"))
    systolic = Column(SMALLINT)
    diastolic = Column(SMALLINT)


class PatientHeartRate(Base, PatientBase):
    __tablename__ = "patient_heart_rate"

    patient_id = Column(ForeignKey("patient_profile.id"))
    heart_rate = Column(SMALLINT)


class PatientRespiratoryRate(Base, PatientBase):
    __tablename__ = "patient_respiratory_rate"

    patient_id = Column(ForeignKey("patient_profile.id"))
    respiratory_rate = Column(SMALLINT)


class PatientBodyTemperature(Base, PatientBase):
    __tablename__ = "patient_body_temperature"

    patient_id = Column(ForeignKey("patient_profile.id"))
    body_temperature = Column(Float)


# Patient Biometrics:
#   PatientBodyWeight
#   PatientHeight
#   PatientBodyMassIndex
class PatientBodyWeight(Base, PatientBase):
    __tablename__ = "patient_body_weight"

    patient_id = Column(ForeignKey("patient_profile.id"))
    body_weight = Column(Float)


class PatientHeight(Base, PatientBase):
    __tablename__ = "patient_height"

    patient_id = Column(ForeignKey("patient_profile.id"))
    height = Column(Float)


class PatientBodyMassIndex(Base, PatientBase):
    __tablename__ = "patient_bmi"

    patient_id = Column(ForeignKey("patient_profile.id"))
    bmi = Column(Float)
    notes = Column(ARRAY(String))


# Patient Family History:
#   PatientFamilyHistory
class PatientFamilyHistory(Base, PatientBase):
    __tablename__ = "patient_family_history"

    patient_id = Column(ForeignKey("patient_profile.id"))
    hypertention = Column(Boolean, default=False)
    t2dm = Column(Boolean, default=False)
    asthma = Column(Boolean, default=False)
    cancer = Column(Boolean, default=False)
    others = Column(ARRAY(String))


# Patient Hospitalization History
#   PatientHospitalizationHistory


class PatientHospitalizationHistory(Base, PatientBase):
    __tablename__ = "patient_hospitalization_history"

    patient_id = Column(ForeignKey("patient_profile.id"))
    chief_complaint = Column(String)
    admission_date = Column(Date)
    discharge_date = Column(Date)
    notes = Column(ARRAY(String))


# Patient Medical History
#   PatientMedicalHistory
class PatientMedicalHistory(Base, PatientBase):
    __tablename__ = "patient_medical_history"

    patient_id = Column(ForeignKey("patient_profile.id"))
    hypertention = Column(Boolean, default=False)
    t2dm = Column(Boolean, default=False)
    asthma = Column(Boolean, default=False)
    cancer = Column(Boolean, default=False)
    others = Column(ARRAY(String))


# Patient Medication Records
#   PatientMedication
class PatientMedication(Base, PatientBase):
    __tablename__ = "patient_medication"

    patient_id = Column(ForeignKey("patient_profile.id"))
    medication = Column(String)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    notes = Column(ARRAY(String), nullable=True)


# Patient OB History
#   PatientOBHistory
class PatientOBHistory(Base, PatientBase):
    __tablename__ = "patient_ob_history"

    patient_id = Column(ForeignKey("patient_profile.id"))
    gravida = Column(SMALLINT)
    para = Column(SMALLINT)
    term = Column(SMALLINT)
    abortion = Column(SMALLINT)
    living = Column(SMALLINT)
    lmp = Column(Date)
    others = Column(ARRAY(String))
    notes = Column(ARRAY(String))


class PatientSurgicalHistory(Base, PatientBase):
    __tablename__ = "patient_surgical_history"

    chief_complaint = Column(String)
    surgery_date = Column(Date)
    notes = Column(ARRAY(String))
