from fastapi import APIRouter, Depends, HTTPException, status
from models.medic import Medic
from database.config import get_db
from sqlalchemy.orm import Session
from auth.dependencies import get_current_user


router = APIRouter(prefix="/medics", tags=["Medics"])


@router.get("/")
def get_medics(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return db.query(Medic).all()
