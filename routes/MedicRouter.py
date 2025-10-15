from fastapi import APIRouter, Depends, status
from database.config import get_db
from sqlalchemy.orm import Session
from utils.role_utils import require_role
from controllers.medic_controller import (
    create_medic as create_medic_controller,
    get_medic_by_id as get_medic_by_id_controller,
    get_medics as get_medics_controller,
    update_medic as update_medic_controller,
    delete_medic as delete_medic_controller,
)
from schemas.medic_schema import MedicCreate
from uuid import UUID, uuid4

router = APIRouter(prefix="/medics", tags=["Medics"])


@router.get(
    "/{medic_id}",
    dependencies=[Depends(require_role("admin"))],
    status_code=status.HTTP_200_OK,
)
def get_medic_by_id(medic_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint que obtiene la información de un médico por su ID.

    Args:
        medic_id: Identificador único del médico.
        db: Sesión de base de datos.

    Usa:
        get_medic_by_id_controller: Función que consulta el médico en la base de datos.

    Roles permitidos:
        admin

    Returns:
        get_medic_by_id_controller: Datos del médico correspondiente al ID proporcionado.
    """
    return get_medic_by_id_controller(db, medic_id)


@router.get(
    "/", dependencies=[Depends(require_role("admin"))], status_code=status.HTTP_200_OK
)
def get_medics(db: Session = Depends(get_db)):
    """
    Endpoint que obtiene todos los médicos registrados en la base de datos.

    Args:
        db: Sesión de base de datos.

    Usa:
        get_medics_controller: Función que consulta todos los médicos.

    Roles permitidos:
        admin

    Returns:
        get_medics_controller: Lista de médicos registrados en la base de datos.
    """

    return get_medics_controller(db)


@router.post(
    "/",
    dependencies=[Depends(require_role("admin"))],
    status_code=status.HTTP_201_CREATED,
)
def create_medic(medic: MedicCreate, db: Session = Depends(get_db)):
    """
    Endpoint que crea un nuevo registro de médico en la base de datos.

    Args:
        medic: Datos del médico a registrar.
        db: Sesión de base de datos.

    Usa:
        create_medic_controller: Función que registra un nuevo médico en la base de datos.

    Roles permitidos:
        admin

    Returns:
        create_medic_controller: Objeto con la información del médico creado.
    """

    return create_medic_controller(db, medic)


@router.put(
    "/{medic_id}",
    dependencies=[Depends(require_role("admin"))],
    status_code=status.HTTP_200_OK,
)
def update_medic(medic_id: UUID, medic: MedicCreate, db: Session = Depends(get_db)):
    """
    Endpoint que actualiza la información de un médico existente en la base de datos.

    Args:
        medic_id: Identificador único del médico a actualizar.
        medic: Datos actualizados del médico.
        db: Sesión de base de datos.

    Usa:
        update_medic_controller: Función que actualiza la información del médico en la base de datos.

    Roles permitidos:
        admin

    Returns:
        update_medic_controller: Objeto con la información actualizada del médico.
    """
    return update_medic_controller(db, medic_id, medic)


@router.delete(
    "/{medic_id}",
    dependencies=[Depends(require_role("admin"))],
    status_code=status.HTTP_200_OK,
)
def delete_medic(medic_id: UUID, db: Session = Depends(get_db)):
    """
    Endpoint que elimina un médico existente de la base de datos.

    Args:
        medic_id: Identificador único del médico a eliminar.
        db: Sesión de base de datos.

    Usa:
        delete_medic_controller: Función que elimina el registro del médico en la base de datos.

    Roles permitidos:
        admin

    Returns:
        delete_medic_controller: Confirmación de eliminación del médico.
    """
    return delete_medic_controller(db, medic_id)
