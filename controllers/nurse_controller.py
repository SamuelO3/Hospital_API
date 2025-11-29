from uuid import uuid4, UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models.nurse import Nurse
from schemas.nurse_schema import Nurse as nurse_schema
from schemas.nurse_schema import NurseUpdate
"""
    Metodos para crear, leer, actualizar y eliminar user_information
"""


def create_nurse(db: Session, nurse: nurse_schema):
    """
    Crea un nuevo enfermera en la base de datos.

    Args
        db:Sesion de la base de datos
        nurse: informacion del enfermera
        token: token del usuario

    return:
        db_user_information: informacion del usuario creada en la db
    """
    new_nurse = Nurse(
        speciality=nurse.speciality,
        id_user_information=nurse.id_user_information,
    )

    db.add(new_nurse)
    db.commit()
    db.refresh(new_nurse)

    return new_nurse


def get_nurse_by_id(db: Session, nurse_id: UUID):
    """
    Obtiene un medico por su id.

    Args
        db:Sesion de la base de datos
        medic_id: id del medico

    return:
        medic: medico encontrado en la db
    """
    return db.query(Nurse).filter(Nurse.id_nurse == nurse_id).first()


def get_nurse(db: Session):
    """
    Obtiene todos los medicos en la base de datos.

    Args
        db:Sesion de la base de datos

    return:
        medicos: lista de medicos en la db
    """
    return db.query(Nurse).all()

def delete_nurse(db: Session, nurse_id: UUID):
    """
    Elimina una enfermera de la base de datos por su ID.

    Args:
        db: Sesión de la base de datos
        nurse_id: ID de la enfermera a eliminar

    Returns:
        dict: mensaje de confirmación o error
    """
    nurse = db.query(Nurse).filter(Nurse.id_nurse == nurse_id).first()

    if not nurse:
        return {"error": "La enfermera no existe."}

    db.delete(nurse)
    db.commit()

    return {"message": "Enfermera eliminada correctamente."}

def update_nurse(db: Session, nurse_id: UUID, payload: NurseUpdate):
    """
    Actualiza una enfermera por su ID.

    Args:
        db: Sesión de la base de datos
        nurse_id: ID de la enfermera a actualizar
        payload: Campos a actualizar (parcial)

    Returns:
        dict: mensaje y/o datos actualizados
    """
    nurse = db.query(Nurse).filter(Nurse.id_nurse == nurse_id).first()
    if not nurse:
        return {"error": "La enfermera no existe."}

    data = payload.dict(exclude_unset=True)

    if "speciality" in data:
        nurse.speciality = data["speciality"]
    if "id_user_information" in data:
        nurse.id_user_information = data["id_user_information"]


    db.add(nurse)
    db.commit()
    db.refresh(nurse)

    return {
        "message": "Enfermera actualizada correctamente.",
        "nurse": nurse
    }