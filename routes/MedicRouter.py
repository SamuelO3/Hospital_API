from fastapi import APIRouter, Depends, HTTPException, status
from models.medic import Medic
from database.config import get_db
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from utils.role_utils import require_role 
from controllers.medic_controller import create_medic as create_medic_controller
from controllers.medic_controller import get_medics as get_medics_controller
from controllers.medic_controller import get_medic_by_id as get_medic_by_id_controller
from controllers.medic_controller import update_medic as update_medic_controller
from controllers.medic_controller import delete_medic as delete_medic_controller
from schemas.medic_schema import MedicCreate
from uuid import UUID, uuid4

router = APIRouter(prefix="/medics", tags=["Medics"])


@router.get("/{medic_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def get_medic_by_id(medic_id: UUID, db: Session = Depends(get_db)):
    return get_medic_by_id_controller(db, medic_id)


@router.get("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def get_medics(db: Session = Depends(get_db)):

    return get_medics_controller(db)


@router.post("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_201_CREATED)
def create_medic( medic: MedicCreate , db: Session = Depends(get_db)):
    return create_medic_controller(db, medic)

@router.put("/{medic_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def update_medic(medic_id: UUID, medic: MedicCreate, db: Session = Depends(get_db)):
    return update_medic_controller(db, medic_id, medic)

@router.delete("/{medic_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def delete_medic(medic_id: UUID, db: Session = Depends(get_db)):
    return delete_medic_controller(db, medic_id)
