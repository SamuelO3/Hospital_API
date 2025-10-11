from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.config import get_db
from schemas.patient_schema import Patient, PatientCreate, PatientUpdate
from utils.role_utils import require_role

from controllers.patient_controller import (
    create_patient as create_patient_controller,
    get_all_patient,
    get_patient_by_id,
    update_patient as update_patient_controller,
    delete_patient as delete_patient_controller,
)


router = APIRouter(prefix="/patient", tags=["Patients"])


@router.post("/", dependencies=[Depends(require_role(["user", "admin"]))])
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):

    try:
        db_patient = create_patient_controller(db, patient)

        return db_patient
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/all",
    response_model=List[Patient],
    dependencies=[Depends(require_role("admin"))],
)
def get_patients(skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):

    try:
        db_patients = get_all_patient(db, limit=limit, skip=skip)

        return db_patients
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{id_patient}", dependencies=[Depends(require_role(["user", "medic", "admin"]))]
)
def get_patient(id_patient: str, db: Session = Depends(get_db)):

    try:
        db_patient = get_patient_by_id(db, id_patient)

        return db_patient
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/update/{id_patient}",
    dependencies=[Depends(require_role(["user", "admin", "medic"]))],
)
def update_patient(
    id_patient: str, update_info: PatientUpdate, db: Session = Depends(get_db)
):
    try:
        db_patient = update_patient_controller(id_patient, update_info, db)

        return db_patient
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/delete/{id_patient}",
    dependencies=[Depends(require_role(["user", "admin"]))],
)
def delete_patient(id_patient: str, db: Session = Depends(get_db)):

    try:
        response = delete_patient_controller(id_patient, db)

        if not response:
            ValueError("Algo salio mal")

        return JSONResponse(
            content={"Response": response}, status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
