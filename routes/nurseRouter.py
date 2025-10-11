from fastapi import APIRouter, Depends, status
from models.nurse import Nurse
from database.config import get_db
from sqlalchemy.orm import Session
from utils.role_utils import require_role
from controllers.nurse_controller import create_nurse as create_nurse_controller
from controllers.nurse_controller import delete_nurse, get_nurse_by_id, update_nurse
from controllers.nurse_controller import get_nurse as get_nurses_controller
from uuid import UUID
from schemas.nurse_schema import NurseCreate, NurseUpdate, Nurse

router = APIRouter(prefix="/nurse", tags=["Nurses"])


@router.get("/{nurse_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def getbyid_nurse(nurse_id: str, db: Session = Depends(get_db)):
    return get_nurse_by_id(db, nurse_id)

@router.get("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def get_nurses(db: Session = Depends(get_db)):
    return get_nurses_controller(db)


@router.post("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_201_CREATED)
def create_nurse(nurse: NurseCreate, db: Session = Depends(get_db)):
    return create_nurse_controller(db, nurse)


@router.delete("/{nurse_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def remove_nurse(nurse_id: str, db: Session = Depends(get_db)):
    return delete_nurse(db, nurse_id)


@router.put("/{nurse_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def update_nurse1(nurse_id: UUID, Nurse: NurseCreate, db: Session = Depends(get_db)):
    return update_nurse(db, nurse_id, Nurse)
