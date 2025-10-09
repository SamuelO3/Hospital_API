from uuid import uuid4
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, session
from auth.JWTHandler import verify_token

from models.medic import Medic
from schemas.medic_schema import Medic as Medic_schema

"""
    Metodos para crear, leer, actualizar y eliminar user_information
"""


def create_medic(db: Session, medic: Medic_schema, token: str = Depends()):
    """
    Crea un nuevo medico en la base de datos.

    Args
        db:Sesion de la base de datos
        medic: informacion del medico
        token: token del usuario

    return:
        db_user_information: informacion del usuario creada en la db
    """

    #! TODO Validacion del Token

    return
