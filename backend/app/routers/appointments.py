from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.services import appointment_service
from typing import List

router = APIRouter()


@router.get("/", response_model=List[AppointmentOut])
def list_appointments(db: Session = Depends(get_db)):
    return appointment_service.get_all(db)


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return appointment_service.get_by_id(db, appointment_id)


@router.get("/patient/{patient_id}", response_model=List[AppointmentOut])
def get_by_patient(patient_id: int, db: Session = Depends(get_db)):
    return appointment_service.get_by_patient(db, patient_id)


@router.get("/doctor/{doctor_id}", response_model=List[AppointmentOut])
def get_by_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return appointment_service.get_by_doctor(db, doctor_id)


@router.post("/", response_model=AppointmentOut, status_code=201)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    return appointment_service.create(db, data)


@router.put("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db)):
    return appointment_service.update(db, appointment_id, data)


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return appointment_service.delete(db, appointment_id)
