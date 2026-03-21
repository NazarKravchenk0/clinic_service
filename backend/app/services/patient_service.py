from sqlalchemy.orm import Session
from app.models.models import Patient
from app.schemas.schemas import PatientCreate, PatientUpdate
from fastapi import HTTPException


def get_all(db: Session):
    return db.query(Patient).all()


def get_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


def create(db: Session, data: PatientCreate):
    existing = db.query(Patient).filter(Patient.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    patient = Patient(**data.dict())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update(db: Session, patient_id: int, data: PatientUpdate):
    patient = get_by_id(db, patient_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient


def delete(db: Session, patient_id: int):
    patient = get_by_id(db, patient_id)
    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted"}
