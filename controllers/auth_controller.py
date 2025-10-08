"""
Controlador de autenticacion para el manejo de tabla User
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Session


from auth.JWTHandler import create_access_token
from auth.security import get_password_hash, verify_password
from models.user import User
from controllers.user_controller import get_user_by_email
from schemas.user_schema import UserCreate, UserResponse


def create_user(db: Session, user: UserCreate):
    """
    Crea un nuevo usuario.

    Args:
        db: Sesión de base de datos
        user: Datos del usuario a crear

    Returns:
        Usuario: Usuario creado
    """
    exists_user = get_user_by_email(db, user.email)
    if exists_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        id_user = uuid4(),
        username=user.username,
        email=user.email,
        password=hashed_password,
        rol_user=user.rol_user,
        active=user.active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def autheticate_user(db: Session, email: str, plain_password: str):
    """
    Autentica un usuario verificando sus credenciales.

    Args:
        db: Sesión de base de datos
        username: Nombre de usuario
        password: Contraseña

    Returns:
        Usuario: Usuario autenticado o None
    """

    user = get_user_by_email(db, email)

    if not user:
        return None
    if not verify_password(plain_password, User.password):
        return None
    if not User.active:
        return None

    return User


def create_token_user(user: User):
    """
    Crea un token JWT para un usuario.

    Args:
        user: Usuario para el cual crear el token

    Returns:
        str: Token JWT
    """
    token_data = {
        "sub": user.username,
        "id_user": str(user.id_user),
        "rol_user": user.rol_user,
    }

    return create_access_token(data=token_data)
