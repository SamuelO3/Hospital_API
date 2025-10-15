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
    """
    EndPoint para obtener una enferma por su id

    Args
        nurse_id: Identificador de la enfermera.
        db: Sección de la db.

    Utiliza
        get_nurse_by_id: Función encargada de consultar en la db la enfermera

    Rol necesario
        admin

    Retorna
        Datos de la enferma que corresponde al nurse_id

    """
    return get_nurse_by_id(db, nurse_id)




@router.get("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def get_nurses(db: Session = Depends(get_db)):
    """
    EndPoint para obtener todas las enfermeras de la db

    Args
        db: Sección de la db.

    Utiliza
    get_nurses_controller: Función para obtener todas las enfermeras

    Rol necesario
        admin

    Retorna
        Datos de las enfermeras

    """

    return get_nurses_controller(db)



@router.post("/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_201_CREATED)
def create_nurse(nurse: NurseCreate, db: Session = Depends(get_db)):
    """
    EndPoint para crear una enfermera

    Args
        db: Sección de la db
        nurse: argumento que llama al NurseCreate del esquema

    Utiliza
    create_nurse_controller: Función para crear una enfermera

    Rol necesario
        admin

    Retorna
        Creación de la enfermera

    """
    return create_nurse_controller(db, nurse)



@router.delete("/{nurse_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def remove_nurse(nurse_id: str, db: Session = Depends(get_db)):
    """
    EndPoint para borrar una enfermera

    Args
        db: Sección de la db
        nurse_id: Atributo necesario para identificar qué enfermera borrar

    Utiliza
    delete_nurse: Función para eliminar una enfermera

    Rol necesario
        admin

    Retorna
        Borra la enferma y devuelve el id de la misma

    """
    return delete_nurse(db, nurse_id)




@router.put("/{nurse_id}", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK)
def update_nurse1(nurse_id: UUID, Nurse: NurseCreate, db: Session = Depends(get_db)):
    """
    EndPoint para actualizar una enfermera

    Args
        db: Sección de la db
        nurse_id: Atributo necesario para identificar qué enfermera actualizar
        Nurse: llama al NurseCreate para los párametros

    Utiliza
    update_nurse: Función para actualizar una enfermera

    Rol necesario
        admin

    Retorna
        Actualiza la enfermera y devuelve todo el cuerpo de la actualización

    """
    return update_nurse(db, nurse_id, Nurse)


