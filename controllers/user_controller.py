"""
Metodos para crear, leer, actualizar y eliminar user
"""

from datetime import datetime
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy.orm import Session

from auth.security import get_password_hash, verify_password
from models.user import User
from schemas.user_schema import UserCreate
from schemas.auth_schema import LoginRequest, UserResponse


def create_user(db: Session, user: UserCreate):
    """
    Crea un nuevo usuario en la base de datos.

    Args
        db:Sesion de la base de datos
        user: Datos del usuario

    return:
        user: usuario creado
    """

    existing_email = get_user_by_email(db, user.email)
    if existing_email:
        raise ValueError("El correo ya esta registrado")

    existing_username = get_user_by_username(db, user.username)
    if existing_username:
        raise ValueError("El nombre de usuario ya existe")

    hashpass = get_password_hash(user.password)
    db_user = User(
        id_user=uuid4(),
        username=user.username,
        password=hashpass,
        email=user.email,
        rol_user=user.rol_user,
        active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_username(db: Session, username: str):
    """
    Obtiene un usuario de la base de datos mediante el usuario

    Args:
        db: sesion de la base de datos
        username: nombre de usuario del usuario a buscar

    return:
        True: si lo encuentra
        Flase: si no lo encuentra
    """

    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """
    Obtiene un usuario de la base de datos mediante el correo

    Args:
        db: sesion de la base de datos
        email: correo del usuario a buscar

    return:
        True: si lo encuentra
        Flase: si no lo encuentra
    """

    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, id_user: str):
    """
    Obtiene un usuario de la base de datos mediante el id

    Args:
        db: sesion de la base de datos
        id_user: id  del usuario a buscar

    return:
        True: si lo encuentra
        Flase: si no lo encuentra
    """

    return db.query(User).filter(User.id_user == id_user).first()


# def update_user(db: Session, id_user: str, update_info: User):
#     """
#     Actualiza un usuario buscado por su id

#     Args:
#         db: Sesion de la base de datos.
#         id_user: id del usuario a actualizar.
#         update_info: nueva informacion del usuario para actualizar
#         token: token del usuario autenticado

#     Return:
#         db_update_user: Usuario actualizado.
#     """

#     #! TODO verificar token

#     db_user = get_user_by_id(db, id_user)

#     if not db_user:
#         raise ValueError("El usuario no existe")

#     if not update_info.username == None:
#         if get_user_by_username(db, update_info.username):
#             raise ValueError("El nombre de usuario ya existe")
#         db_user.username = update_info.username

#     if not update_info.password == None:
#         db_user = get_password_hash(update_info.password)

#     if not update_info.email == None:
#         if get_user_by_email(db, update_info.email):
#             raise ValueError("El correo ya esta en uso")
#         db_user.email = update_info.email

#     db_user.updated_at = datetime.now()

#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)

#     return db_user

# controllers/user_controller.py
from datetime import datetime
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.user import User
from auth.security import get_password_hash
from .user_controller import get_user_by_id, get_user_by_username, get_user_by_email
import json

def update_user(db: Session, id_user: str, update_info):
    # — Normalización del payload —
    if isinstance(update_info, BaseModel):
        data = update_info.model_dump(exclude_unset=True)
    elif isinstance(update_info, dict):
        data = {k: v for k, v in update_info.items() if v is not None}
    elif isinstance(update_info, str):
        try:
            data = json.loads(update_info)
        except Exception:
            raise ValueError("Body inválido: se esperaba JSON (Content-Type: application/json).")
    else:
        # objeto con atributos
        data = {}
        for k in ("username", "email", "password"):
            if hasattr(update_info, k):
                v = getattr(update_info, k)
                if v is not None:
                    data[k] = v

    db_user = get_user_by_id(db, id_user)
    if not db_user:
        raise ValueError("El usuario no existe")

    # username
    new_username = data.get("username")
    if new_username is not None and new_username != db_user.username:
        if get_user_by_username(db, new_username):
            raise ValueError("El nombre de usuario ya existe")
        db_user.username = new_username

    # email
    new_email = data.get("email")
    if new_email is not None and new_email != db_user.email:
        if get_user_by_email(db, new_email):
            raise ValueError("El correo ya esta en uso")
        db_user.email = new_email

    # password
    new_password = data.get("password")
    if new_password:
        db_user.password = get_password_hash(new_password)

    db_user.updated_at = datetime.now()
    db.add(db_user); db.commit(); db.refresh(db_user)
    return db_user

