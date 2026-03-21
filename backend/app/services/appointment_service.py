from sqlalchemy.orm import Session, joinedload
from app.models.models import Appointment
from app.schemas.schemas import AppointmentCreate, AppointmentUpdate
from fastapi import HTTPException


def get_all(db: Session):
    return db.query(Appointment).options(
        joinedload(Appointment.patient),
        joinedload(Appointment.doctor)
    ).all()


def get_by_id(db: Session, appointment_id: int):
    appointment = db.query(Appointment).options(
        joinedload(Appointment.patient),
        joinedload(Appointment.doctor)
    ).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


def get_by_patient(db: Session, patient_id: int):
    return db.query(Appointment).options(
        joinedload(Appointment.patient),
        joinedload(Appointment.doctor)
    ).filter(Appointment.patient_id == patient_id).all()


def get_by_doctor(db: Session, doctor_id: int):
    return db.query(Appointment).options(
        joinedload(Appointment.patient),
        joinedload(Appointment.doctor)
    ).filter(Appointment.doctor_id == doctor_id).all()


def create(db: Session, data: AppointmentCreate):
    appointment = Appointment(**data.dict())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return get_by_id(db, appointment.id)


def update(db: Session, appointment_id: int, data: AppointmentUpdate):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(appointment, key, value)
    db.commit()
    return get_by_id(db, appointment_id)


def delete(db: Session, appointment_id: int):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"detail": "Appointment deleted"}
