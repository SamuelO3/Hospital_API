from uuid import uuid4
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, session
from auth.JWTHandler import verify_token

from models.user_information import UserInformation
from schemas.user_information_schema import UserInformation as Information_schema

"""
    Metodos para crear, leer, actualizar y eliminar user_information
"""


def create_user_information(
    db: session, information: Information_schema, token: str = Depends()
):
    """
    Crea una nueva informacion de usuario en la base de datos.

    Args
        db:Sesion de la base de datos
        information: informacion del usuario
        token: Token del usuario

    return:
        db_user_information: informacion del usuario creada en la db
    """

    #! TODO validacion de autenticacion

    exist_information = get_information_by_document_number(
        db, information.document_number_user
    )
    if exist_information:
        raise ValueError("Este documento ya se encuentra registrado")

    db_user_information = Information_schema(
        id_user_information=uuid4(),
        first_name_user=information.first_name_user,
        second_name_user=information.second_name_user,
        first_lastname_user=information.first_lastname_user,
        second_lastname_user=information.second_lastname_user,
        birth_date_user=information.birth_date_user,
        gender_user=information.second_name_user,
        phone_number_user=information.phone_number_user,
        document_number_user=information.document_number_user,
        id_user=str(information.id_user),
    )

    db.add(db_user_information)
    db.commit()
    db.refresh(db_user_information)
    return db_user_information


def update_user_information(
    db: Session, update_info: Information_schema, id: str, token: str = Depends()
):
    """
    Actualiza informacion del usuario mediante el id

    Args:
        db: Sesion de la base de datos
        update_info: informacion para actualizar la db
        token: token del usuario validado

    return:
        informacion del usuario actualizada
    """

    #! TODO validacion de autenticacion

    db_user_information = get_information_by_id(db, id)
    if not db_user_information:
        raise ValueError("No existe la informacion de usuario para este id")

    db_user_information.first_name_user = update_info.first_name_user
    db_user_information.second_name_user = update_info.second_name_user
    db_user_information.first_lastname_user = update_info.first_lastname_user
    db_user_information.second_lastname_user = update_info.second_lastname_user
    db_user_information.birth_date_user = update_info.birth_date_user
    db_user_information.gender_user = update_info.gender_user
    db_user_information.phone_number_user = update_info.phone_number_user
    db_user_information.document_number_user = update_info.document_number_user

    db.add(db_user_information)
    db.commit()
    db.refresh(db_user_information)
    return db_user_information


def get_all_users_information(
    db: Session, skip: int = 0, limit: int = 30, token: str = Depends()
):
    """
    Obtiene informacion del usuario mediante el documento de identidad

    Args:
        db: Sesion de la base de datos
        document_number: documento a buscar en la db
        token: token del usuario validado

    return:
        informacion del usuario
    """

    #! TODO validacion de autenticacion
    return db.query(UserInformation).offset(skip).limit(limit).all()


def get_information_by_document_number(
    db: Session, document_number: str, token: str = Depends()
):
    """
    Obtiene informacion del usuario mediante el documento de identidad

    Args:
        db: Sesion de la base de datos
        document_number: documento a buscar en la db
        token: token del usuario validado

    return:
        informacion del usuario
    """

    #! TODO validacion de autenticacion

    return (
        db.query(UserInformation)
        .filter(UserInformation.document_number_user == document_number)
        .first()
    )


def get_information_by_id(db: Session, id_information: str, token: str = Depends()):
    """
    Obtiene informacion del usuario mediante el id

    Args:
        db: Sesion de la base de datos
        id: id a buscar en la db
        token: token del usuario validado

    return:
        informacion del usuario
    """

    #! TODO validacion de autenticacion

    return (
        db.query(UserInformation)
        .filter(UserInformation.id_user_information == id_information)
        .first()
    )


def delete_user_information(db: Session, id_information: str, token: str = Depends()):
    """
    Elimina informacion del usuario mediante el id

    Args:
        db: Sesion de la base de datos
        id: id de la informacion de usuario a eliminar en la db
        token: token del usuario validado

    return:
        bool True si fue eliminado
    """

    #! TODO validacion de autenticacion

    user_information_to_delete = get_information_by_id(db, id_information)
    if not user_information_to_delete:
        raise ValueError("No existe la informacion de usuario en la db")

    db.delete(user_information_to_delete)
    db.commit()
    return True
