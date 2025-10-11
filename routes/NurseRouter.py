from fastapi import APIRouter, Depends, HTTPException, status
from models.nurse import Nurse
from database.config import get_db
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from utils.role_utils import require_role 
from controllers.Nurse_Controller import create_nurse as create_nurse_controller
from controllers.Nurse_Controller import delete_nurse, get_nurse_by_id, update_nurse
from schemas.medic_schema import MedicCreate
from uuid import uuid4, UUID
from schemas.nurse_schema import NurseUpdate

router = APIRouter(prefix="/nurse", tags=["Nurses"])


@router.get("/")
def get_nurses(db: Session = Depends(get_db)):
    return db.query(Nurse).all()

@router.post("/", dependencies=[Depends(require_role("admin"))])
def create_nurse( medic: MedicCreate , db: Session = Depends(get_db)):
    return create_nurse_controller(db, medic)

@router.delete("delete/{nurse_id}", dependencies=[Depends(require_role("admin"))] )
def remove_nurse(nurse_id: UUID, db: Session = Depends(get_db)):
    return delete_nurse(db, nurse_id)

@router.get("byid/{nurse_id}", dependencies=[Depends(require_role("admin"))])
def getbyid_nurse(nurse_id: UUID, db: Session = Depends(get_db)):
    return get_nurse_by_id(db, nurse_id)

@router.put("update/{nurse_id}", dependencies=[Depends(require_role("admin"))])
def update_nurse1(nurse_id: UUID, body: NurseUpdate, db: Session = Depends(get_db)):
    return update_nurse(db, nurse_id, body)