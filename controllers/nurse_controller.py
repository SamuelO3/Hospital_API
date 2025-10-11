from uuid import uuid4, UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models.nurse import Nurse as Nurse_model
from schemas.nurse_schema import Nurse as NurseCreate
from schemas.nurse_schema import NurseUpdate
from schemas.nurse_schema import NurseBase

"""
    Metodos para crear, leer, actualizar y eliminar user_information
"""


def create_nurse(db: Session, nurse: NurseCreate):
    """
    Crea un nuevo enfermera en la base de datos.

    Args
        db:Sesion de la base de datos
        nurse: informacion del enfermera
        token: token del usuario

    return:
        db_user_information: informacion del usuario creada en la db
    """
    new_nurse = Nurse_model(
        speciality=nurse.speciality,
        id_user_information=nurse.id_user_information,
    )

    db.add(new_nurse)
    db.commit()
    db.refresh(new_nurse)

    return new_nurse


def get_nurse_by_id(db: Session, nurse_id: str):
    """
    Obtiene un enfermera por su id.

    Args
        db:Sesion de la base de datos
        nurse_id: id del enfermera

    return:
        nurse: enfermera encontrado en la db
    """
    nurse = db.query(Nurse_model).filter(Nurse_model.id_nurse ==  nurse_id).first()
    if nurse:
        return nurse
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Nurse with id '{nurse_id}' not found")


def get_nurse(db: Session):
    """
    Obtiene todos los enfermeras en la base de datos.

    Args
        db:Sesion de la base de datos

    return:
        enfermeras: lista de enfermeras en la db
    """
    nurses = db.query(Nurse_model).all()
    if nurses:
        return nurses
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron enfermeras")


def delete_nurse(db: Session, nurse_id: str):
    """
    Elimina una enfermera de la base de datos por su ID.

    Args:
        db: Sesión de la base de datos
        nurse_id: ID de la enfermera a eliminar

    Returns:
        dict: mensaje de confirmación o error
    """
    nurse_to_delete = get_nurse_by_id(db, nurse_id)
    if nurse_to_delete:
        
        try:
            user_info = nurse_to_delete.nurse_information  
            db.delete(nurse_to_delete)
            if user_info:
                user = user_info.user
                if user:
                    db.delete(user_info)
                    db.delete(user)
                else:
                    db.delete(user_info)
                
            
            db.commit()
            return nurse_to_delete
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise 


def update_nurse(db: Session, nurse_id: str, nurse: NurseCreate):
    """
    Actualiza una enfermera por su ID.

    Args:
        db: Sesión de la base de datos
        nurse_id: ID de la enfermera a actualizar
        payload: Campos a actualizar (parcial)

    Returns:
        dict: mensaje y/o datos actualizados
    """
    nurse_to_update = get_nurse_by_id(db, nurse_id)
    if nurse_to_update:
        try:
            nurse_to_update.speciality = nurse.speciality
            nurse_to_update.id_user_information = nurse.id_user_information
            db.commit()
            db.refresh(nurse_to_update)
            return nurse_to_update
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise