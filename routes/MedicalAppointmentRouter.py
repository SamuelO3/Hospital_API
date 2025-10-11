from fastapi import APIRouter, Depends, HTTPException, status
from models.medic import Medic
from database.config import get_db
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from utils.role_utils import require_role 
from controllers.medical_appointmentController import create_medical_appointment as create_medical_appointmentC
from controllers.medical_appointmentController import get_medical_appointment as get_medical_appointmentC
from controllers.medical_appointmentController import get_medical_appointment_by_id as get_medical_appointmentCI
from controllers.medical_appointmentController import update_medical_appointment as update_medical_appointmentC
from controllers.medical_appointmentController import delete_medical_appointment as delete_medical_appointmentC
from schemas.medical_appointment_schema import MedicalAppointmentCreate as mac
from uuid import UUID, uuid4

router = APIRouter(prefix="/MedicalApp", tags=["MedicalApp"])


@router.get("/{mpp_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def get_mpp_by_id(mpp_id: str, db: Session = Depends(get_db)):
    return get_medical_appointmentCI(db, mpp_id)


@router.get("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def get_mpp(db: Session = Depends(get_db)):

    return get_medical_appointmentC(db)


@router.post("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_201_CREATED)
def create_medic( Mac: mac , db: Session = Depends(get_db)):
    return create_medical_appointmentC(db, Mac)

@router.put("/{mpp_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def update_medic(mpp_id: str, Mac: mac, db: Session = Depends(get_db)):
    return update_medical_appointmentC(db, mpp_id, Mac)

@router.delete("/{mpp_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def delete_medic(mpp_id: str, db: Session = Depends(get_db)):
    return delete_medical_appointmentC(db, mpp_id)
