from datetime import datetime
from typing import List

from sqlalchemy import (
    ARRAY,
    SMALLINT,
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship

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


class PatientAppointments(Base, PatientBase):
    __tablename__ = "patient_appointments"

    account_id = Column(ForeignKey("medrekk_accounts.id"))
    patient_id = Column(ForeignKey("patient_profile.id"))
    appointment_date = Column(Date, nullable=False)


class PatientVisit(Base, PatientBase):
    __tablename__ = "patient_visits"

    account_id = Column(ForeignKey("medrekk_accounts.id"))
    patient_id = Column(ForeignKey("patient_profile.id"))
    appointment_id = Column(ForeignKey("patient_appointments.id"))
    visit_date = Column(Date, nullable=False)

    __table_args__ = (
        Index("idx_patient_visit", "patient_id", "visit_date"),
        UniqueConstraint("patient_id", "visit_date", name="uc_patient_visit"),
    )


class PatientRecord(Base, PatientBase):
    __tablename__ = "patient_records"

    account_id = Column(ForeignKey("medrekk_accounts.id"))
    patient_id = Column(ForeignKey("patient_profile.id"))
    chief_complaint = Column(ARRAY(String))

    diagnosis: Mapped[List["PatientDiagnosis"]] = relationship(backref="record")
    body_temperatures: Mapped[List["PatientBodyTemperature"]] = relationship(
        backref="record"
    )


class PatientDiagnosis(Base, PatientBase):
    __tablename__ = "patient_diagnosis"

    record_id = Column(ForeignKey("patient_records.id"))
    diagnosis_code = Column(String)
    diagnosis_description = Column(String)


# Patient Vitals:
#   PatientBloodPressure,
#   PatientHeartRate,
#   PatientRespiratoryRate,
#   PatientBodyTemperature
class PatientBloodPressure(Base, PatientBase):
    __tablename__ = "patient_blood_pressure"

    record_id = Column(ForeignKey("patient_records.id"))
    dt_measured = Column(DateTime)
    systolic = Column(SMALLINT)
    diastolic = Column(SMALLINT)

    __table_args__ = (
        UniqueConstraint(
            "record_id", "dt_measured", name="uc_bloodpressure_patient_dt"
        ),
        Index("idx_bloodpressure_patient_dt", "record_id", "dt_measured"),
    )


class PatientHeartRate(Base, PatientBase):
    __tablename__ = "patient_heart_rate"

    record_id = Column(ForeignKey("patient_records.id"))
    dt_measured = Column(DateTime)
    heart_rate = Column(SMALLINT)

    __table_args__ = (
        UniqueConstraint("record_id", "dt_measured", name="uc_heartrate_patient_dt"),
        Index("idx_heartrate_patient_dt", "record_id", "dt_measured"),
    )


class PatientRespiratoryRate(Base, PatientBase):
    __tablename__ = "patient_respiratory_rate"

    record_id = Column(ForeignKey("patient_records.id"))
    dt_measured = Column(DateTime)
    respiratory_rate = Column(SMALLINT)

    __table_args__ = (
        UniqueConstraint(
            "record_id", "dt_measured", name="uc_respiratoryrate_patient_dt"
        ),
        Index("idx_respiratoryrate_patient_dt", "record_id", "dt_measured"),
    )


class PatientBodyTemperature(Base, PatientBase):
    __tablename__ = "patient_body_temperature"

    record_id = Column(ForeignKey("patient_records.id"))
    dt_measured = Column(DateTime)
    body_temperature = Column(Float)

    __table_args__ = (
        UniqueConstraint(
            "record_id", "dt_measured", name="uc_bodytemperature_patient_dt"
        ),
    )


# Patient Biometrics:
#   PatientBodyWeight
#   PatientHeight
#   PatientBodyMassIndex
class PatientBodyWeight(Base, PatientBase):
    __tablename__ = "patient_body_weight"

    patient_id = Column(ForeignKey("patient_profile.id"))
    date_measured = Column(Date)
    body_weight = Column(Float)

    __table_args__ = (
        UniqueConstraint(
            "patient_id", "date_measured", name="uc_bodyweight_patient_date"
        ),
    )


class PatientHeight(Base, PatientBase):
    __tablename__ = "patient_height"

    patient_id = Column(ForeignKey("patient_profile.id"))
    date_measured = Column(Date)
    height = Column(Float)

    __table_args__ = (
        UniqueConstraint("patient_id", "date_measured", name="uc_height_patient_date"),
    )


class PatientBodyMassIndex(Base, PatientBase):
    __tablename__ = "patient_bmi"

    patient_id = Column(ForeignKey("patient_profile.id"))
    date_measured = Column(Date)
    bmi = Column(Float)
    notes = Column(ARRAY(String))

    __table_args__ = (
        UniqueConstraint("patient_id", "date_measured", name="uc_bmi_patient_date"),
    )


# Patient Family History:
#   PatientFamilyHistory
class PatientFamilyHistory(Base, PatientBase):
    __tablename__ = "patient_family_history"

    patient_id = Column(ForeignKey("patient_profile.id"), unique=True)
    hypertension = Column(Boolean, default=False)
    t2dm = Column(Boolean, default=False)
    asthma = Column(Boolean, default=False)
    cancer = Column(Boolean, default=False)
    others = Column(ARRAY(String))
    notes = Column(ARRAY(String))


# Patient Medical History
#   PatientMedicalHistory
class PatientMedicalHistory(Base, PatientBase):
    __tablename__ = "patient_medical_history"

    patient_id = Column(ForeignKey("patient_profile.id"), unique=True)
    hypertension = Column(Boolean, default=False)
    t2dm = Column(Boolean, default=False)
    asthma = Column(Boolean, default=False)
    cancer = Column(Boolean, default=False)
    others = Column(ARRAY(String))
    notes = Column(ARRAY(String))


# Patient OB History
#   PatientOBHistory
class PatientOBHistory(Base, PatientBase):
    __tablename__ = "patient_ob_history"

    patient_id = Column(ForeignKey("patient_profile.id"), unique=True)
    gravida = Column(SMALLINT)
    para = Column(SMALLINT)
    term = Column(SMALLINT)
    abortion = Column(SMALLINT)
    living = Column(SMALLINT)
    lmp = Column(Date)
    others = Column(ARRAY(String))
    notes = Column(ARRAY(String))


# Patient Hospitalization History
#   PatientHospitalizationHistory


class PatientHospitalizationHistory(Base, PatientBase):
    __tablename__ = "patient_hospitalization_history"

    patient_id = Column(ForeignKey("patient_profile.id"))
    chief_complaint = Column(String)
    admission_date = Column(Date)
    discharge_date = Column(Date)
    notes = Column(ARRAY(String))


class PatientSurgicalHistory(Base, PatientBase):
    __tablename__ = "patient_surgical_history"

    patient_id = Column(ForeignKey("patient_profile.id"))
    chief_complaint = Column(String)
    surgery_date = Column(Date)
    notes = Column(ARRAY(String))


# Patient Medication Records
#   PatientMedication
class PatientMedication(Base, PatientBase):
    __tablename__ = "patient_medication"

    patient_id = Column(ForeignKey("patient_profile.id"))
    medication = Column(String)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    notes = Column(ARRAY(String), nullable=True)


class PatientAllergy(Base, PatientBase):
    __tablename__ = "patient_allergy"

    patient_id = Column(ForeignKey("patient_profile.id"))
    allergen = Column(String)
    reaction_description = Column(String)
    notes = Column(ARRAY(String), nullable=True)


class PatientImmunization(Base, PatientBase):
    __tablename__ = "patient_immunization"

    patient_id = Column(ForeignKey("patient_profile.id"))
    vaccine = Column(String)
    date_administered = Column(Date)
    notes = Column(ARRAY(String), nullable=True)
