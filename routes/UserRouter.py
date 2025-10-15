# routes/UserRouter.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from database.config import get_db
from utils.role_utils import require_role
from schemas.user_schema import UserCreate, UserUpdate
from schemas.auth_schema import UserResponse
from controllers.user_controller import (
    create_user,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    update_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    dependencies=[Depends(require_role("admin"))],
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    """
    Descripcion:
        Crea un nuevo usuario en la base de datos.

    Args:
        user (UserCreate): Datos del nuevo usuario a registrar.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        create_user(db, user)

    Returns:
        UserResponse: Datos del usuario creado exitosamente.
    """
    try:
        db_user = create_user(db, user)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_user


@router.get(
    "/{id_user}",
    dependencies=[Depends(require_role("admin"))],
    response_model=Optional[UserResponse],
)
def get_userbyid(id_user: UUID, db: Session = Depends(get_db)):
    """
    Descripcion:
        Obtiene la información de un usuario específico mediante su identificador único.

    Args:
        id_user (UUID): Identificador único del usuario.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        get_user_by_id(db, id_user)

    Returns:
        Optional[UserResponse]: Datos del usuario encontrado o None si no existe.
    """
    try:
        db_user = get_user_by_id(db, id_user)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_user


@router.get(
    "/by-username/{username}",
    dependencies=[Depends(require_role("admin"))],
    response_model=Optional[UserResponse],
)
def get_userbyusername(username: str, db: Session = Depends(get_db)):
    """
    Descripcion:
        Busca un usuario por su nombre de usuario (username).

    Args:
        username (str): Nombre de usuario a consultar.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        get_user_by_username(db, username)

    Returns:
        Optional[UserResponse]: Datos del usuario encontrado o None si no existe.
    """
    try:
        db_user = get_user_by_username(db, username)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return db_user


@router.get(
    "/by-email/{email}",
    dependencies=[Depends(require_role("admin"))],
    response_model=Optional[UserResponse],
)
def get_userbyemail(email: str, db: Session = Depends(get_db)):
    """
    Descripcion:
        Busca un usuario por su correo electrónico.

    Args:
        email (str): Correo electrónico del usuario a consultar.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        get_user_by_email(db, email)

    Returns:
        Optional[UserResponse]: Datos del usuario encontrado o None si no existe.
    """
    try:
        db_user = get_user_by_email(db, email)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return db_user


@router.put(
    "/{id_user}",
    dependencies=[Depends(require_role("admin"))],
    response_model=UserResponse,
)
def update_userbyid(id_user: UUID, body: UserUpdate, db: Session = Depends(get_db)):
    """
    Descripcion:
        Actualiza la información de un usuario existente en la base de datos.

    Args:
        id_user (UUID): Identificador único del usuario a actualizar.
        body (UserUpdate): Datos nuevos del usuario.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        update_user(db, id_user, body)

    Returns:
        UserResponse: Datos actualizados del usuario.
    """
    try:
        db_user = update_user(db, id_user, body)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_user
