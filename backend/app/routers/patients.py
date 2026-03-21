from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import PatientCreate, PatientUpdate, PatientOut
from app.services import patient_service
from typing import List

router = APIRouter()


@router.get("/", response_model=List[PatientOut])
def list_patients(db: Session = Depends(get_db)):
    return patient_service.get_all(db)


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return patient_service.get_by_id(db, patient_id)


@router.post("/", response_model=PatientOut, status_code=201)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    return patient_service.create(db, data)


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, data: PatientUpdate, db: Session = Depends(get_db)):
    return patient_service.update(db, patient_id, data)


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    return patient_service.delete(db, patient_id)
