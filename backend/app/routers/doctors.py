from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import DoctorCreate, DoctorUpdate, DoctorOut
from app.services import doctor_service
from typing import List

router = APIRouter()


@router.get("/", response_model=List[DoctorOut])
def list_doctors(db: Session = Depends(get_db)):
    return doctor_service.get_all(db)


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctor_service.get_by_id(db, doctor_id)


@router.post("/", response_model=DoctorOut, status_code=201)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_service.create(db, data)


@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(doctor_id: int, data: DoctorUpdate, db: Session = Depends(get_db)):
    return doctor_service.update(db, doctor_id, data)


@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctor_service.delete(db, doctor_id)
