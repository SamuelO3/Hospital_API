from uuid import uuid4, UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

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
    return db.query(Medic).filter(Medic.id_medic == medic_id).first()


def get_medics(db: Session):
    """
    Obtiene todos los medicos en la base de datos.

    Args
        db:Sesion de la base de datos

    return:
        medicos: lista de medicos en la db
    """
    return db.query(Medic).all()