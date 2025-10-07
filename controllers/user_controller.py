from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from auth.JWTHandler import create_access_token, get_password_hash, verify_password
from models.user import User
from schemas.auth_schema import LoginRequest, UserCreate, UserResponse


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
        rol=user.rol_user,
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
