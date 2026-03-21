from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.models import AppointmentStatus


# --- Patient Schemas ---
class PatientBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None


class PatientOut(PatientBase):
    id: int

    class Config:
        from_attributes = True


# --- Doctor Schemas ---
class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    email: str
    phone: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None


class DoctorOut(DoctorBase):
    id: int

    class Config:
        from_attributes = True


# --- Appointment Schemas ---
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[str] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None


class AppointmentOut(AppointmentBase):
    id: int
    status: AppointmentStatus
    patient: PatientOut
    doctor: DoctorOut

    class Config:
        from_attributes = True
