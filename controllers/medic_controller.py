from uuid import uuid4, UUID
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.medic import Medic
from schemas.medic_schema import Medic as Medic_schema

"""
    Metodos para crear, leer, actualizar y eliminar user_information
"""


def create_medic(db: Session, medic: Medic_schema):
    """
    Crea un nuevo medico en la base de datos.

    Args
        db:Sesion de la base de datos
        medic: informacion del medico
        token: token del usuario

    return:
        db_user_information: informacion del usuario creada en la db
    """
    new_medic = Medic(
        specialty=medic.specialty,
        id_user_information=medic.id_user_information,
    )

    db.add(new_medic)
    db.commit()
    db.refresh(new_medic)

    return new_medic


def get_medic_by_id(db: Session, medic_id: UUID):
    """
    Obtiene un medico por su id.

    Args
        db:Sesion de la base de datos
        medic_id: id del medico

    return:
        medic: medico encontrado en la db
    """
    medic = db.query(Medic).filter(Medic.id_medic == medic_id).first()
    if medic:
        return medic
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medic with id '{medic_id}' not found")


def get_medics(db: Session):
    """
    Obtiene todos los medicos en la base de datos.

    Args
        db:Sesion de la base de datos

    return:
        medicos: lista de medicos en la db
    """
    medicos = db.query(Medic).all()
    if medicos:
        return medicos
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron medicos")


def update_medic(db: Session, medic_id: UUID, medic: Medic_schema):
    """
    Actualiza un medico en la base de datos.

    Args
        db:Sesion de la base de datos
        medic_id: id del medico
        medic: informacion del medico

    return:
        medic: medico actualizado en la db
    """
    medic_to_update = get_medic_by_id(db, medic_id)
    if medic_to_update:
        try:
            medic_to_update.specialty = medic.specialty
            medic_to_update.id_user_information = medic.id_user_information
            db.commit()
            db.refresh(medic_to_update)
            return medic_to_update
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise


def delete_medic(db: Session, medic_id: UUID):
    """
    Elimina un medico de la base de datos.

    Args
        db:Sesion de la base de datos
        medic_id: id del medico

    return:
        medic: medico eliminado de la db
    """
    medic_to_delete = get_medic_by_id(db, medic_id)
    if medic_to_delete:
        try:
            db.delete(medic_to_delete)
            db.commit()
            return medic_to_delete
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise 
