from fastapi import APIRouter, Depends, HTTPException, status
from models.medic import Medic
from database.config import get_db
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user
from utils.role_utils import require_role 
from controllers.medic_controller import create_medic as create_medic_controller
from schemas.medic_schema import MedicCreate


router = APIRouter(prefix="/medics", tags=["Medics"])


@router.get("/")
def get_medics(db: Session = Depends(get_db)):

    return db.query(Medic).all()

@router.post("/", dependencies=[Depends(require_role("admin"))])
def create_medic( medic: MedicCreate , db: Session = Depends(get_db)):
    return create_medic_controller(db, medic)

