from fastapi import APIRouter, Depends, HTTPException, status
from models.nurse import Nurse
from database.config import get_db
from sqlalchemy.orm import Session
from utils.role_utils import require_role
from controllers.nurse_controller import (
    create_nurse as create_nurse_controller,
    get_nurse_by_id as get_nurse_by_id_controller,
    delete_nurse as delete_nurse_controller,
    update_nurse as update_nurse_controller,
)
from schemas.nurse_schema import NurseCreate
from uuid import UUID
from schemas.nurse_schema import NurseCreate, NurseUpdate

router = APIRouter(prefix="/nurse", tags=["Nurses"])


@router.get("/")
def get_nurses(db: Session = Depends(get_db)):
    return db.query(Nurse).all()

@router.post("/", dependencies=[Depends(require_role("admin"))])
def create_nurse(nurse: NurseCreate, db: Session = Depends(get_db)):
    """
    Descripcion:
        Crea un nuevo registro de enfermero en la base de datos.

    Args:
        medic (MedicCreate): Datos del enfermero a registrar.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        create_nurse_controller(db, nurse).

    Returns:
        Nurse: Objeto con los datos del enfermero creado.
    """
    return create_nurse_controller(db, nurse)


@router.delete("delete/{nurse_id}", dependencies=[Depends(require_role("admin"))] )
def remove_nurse(nurse_id: UUID, db: Session = Depends(get_db)):
    return delete_nurse(db, nurse_id)

@router.get("byid/{nurse_id}", dependencies=[Depends(require_role("admin"))])
def getbyid_nurse(nurse_id: UUID, db: Session = Depends(get_db)):
    return get_nurse_by_id(db, nurse_id)

@router.put("update/{nurse_id}", dependencies=[Depends(require_role("admin"))])
def update_nurse1(nurse_id: UUID, body: NurseUpdate, db: Session = Depends(get_db)):
    return update_nurse(db, nurse_id, body)