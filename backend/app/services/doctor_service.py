from sqlalchemy.orm import Session
from app.models.models import Doctor
from app.schemas.schemas import DoctorCreate, DoctorUpdate
from fastapi import HTTPException


def get_all(db: Session):
    return db.query(Doctor).all()


def get_by_id(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def create(db: Session, data: DoctorCreate):
    existing = db.query(Doctor).filter(Doctor.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    doctor = Doctor(**data.dict())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def update(db: Session, doctor_id: int, data: DoctorUpdate):
    doctor = get_by_id(db, doctor_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor


def delete(db: Session, doctor_id: int):
    doctor = get_by_id(db, doctor_id)
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted"}
