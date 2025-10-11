from fastapi import APIRouter, Depends
from models.nurse import Nurse
from database.config import get_db
from sqlalchemy.orm import Session
from utils.role_utils import require_role
from controllers.nurse_controller import create_nurse as create_nurse_controller
from controllers.nurse_controller import delete_nurse, get_nurse_by_id, update_nurse
from controllers.nurse_controller import get_nurse as get_nurses_controller
from uuid import UUID
from schemas.nurse_schema import NurseCreate, NurseUpdate

router = APIRouter(prefix="/nurse", tags=["Nurses"])


@router.get("/")
def get_nurses(db: Session = Depends(get_db), skip: int = 0, limit: int = 15):
    return get_nurses_controller(db, skip, limit)


@router.post("/", dependencies=[Depends(require_role("admin"))])
def create_nurse(nurse: NurseCreate, db: Session = Depends(get_db)):
    return create_nurse_controller(db, nurse)


@router.delete("delete/{nurse_id}", dependencies=[Depends(require_role("admin"))])
def remove_nurse(nurse_id: UUID, db: Session = Depends(get_db)):
    return delete_nurse(db, nurse_id)


@router.get("byid/{nurse_id}", dependencies=[Depends(require_role("admin"))])
def getbyid_nurse(nurse_id: UUID, db: Session = Depends(get_db)):
    return get_nurse_by_id(db, nurse_id)


@router.put("update/{nurse_id}", dependencies=[Depends(require_role("admin"))])
def update_nurse1(nurse_id: UUID, body: NurseUpdate, db: Session = Depends(get_db)):
    return update_nurse(db, nurse_id, body)
