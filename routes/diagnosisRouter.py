from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.config import get_db
from utils.role_utils import require_role

from controllers.diagnosis_controller import (
    create_diagnosis as create_diagnosis_controller,
    get_all_diagnosis as get_all_diagnosis_controller,
    get_diagnosis_by_id as get_diagnosis_by_id_controller,
    update_diagnosis as update_diagnosis_controller,
    delete_diagnosis as delete_diagnosis_controller,
)
from schemas.diagnosis_schema import DiagnosisCreate, DiagnosisUpdate


router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])


@router.post("/", dependencies=[Depends(require_role(["admin", "medic"]))])
def create_diagnosis(diagnosis: DiagnosisCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo diagnóstico en la base de datos.

    Args:
        diagnosis (DiagnosisCreate): Datos del diagnóstico a registrar.
        db (Session): Sesión de base de datos proporcionada por la dependencia get_db().

    Usa:
        create_diagnosis_controller(): Función que registra el diagnóstico en la base de datos.

    Roles requeridos:
        admin, medic

    Returns:
        Diagnosis: Objeto con la información del diagnóstico creado o un error HTTP 400 si ocurre una excepción.
    """
    try:
        db_diagnosis = create_diagnosis_controller(diagnosis, db)
        return db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/all", dependencies=[Depends(require_role(["admin", "medic"]))])
def get_all_diagnosis(db: Session = Depends(get_db), skip: int = 0, limit: int = 15):
    """
    Obtiene una lista paginada de todos los diagnósticos registrados.

    Args:
        db (Session): Sesión de base de datos proporcionada por la dependencia get_db().
        skip (int): Número de registros a omitir para la paginación. Por defecto 0.
        limit (int): Número máximo de registros a devolver. Por defecto 15.

    Usa:
        get_all_diagnosis_controller(): Función que consulta todos los diagnósticos.

    Roles requeridos:
        admin, medic

    Returns:
        list_db_diagnosis: Lista de diagnósticos o un error HTTP 400 si ocurre una excepción.
    """
    try:
        list_db_diagnosis = get_all_diagnosis_controller(db, skip, limit)
        return list_db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/{id_diagnosis}", dependencies=[Depends(require_role(["admin", "medic"]))])
def get_diagnosis(id_diagnosis: str, db: Session = Depends(get_db)):
    """
    Obtiene la información de un diagnóstico específico por su ID.

    Args:
        id_diagnosis (str): Identificador único del diagnóstico.
        db (Session): Sesión de base de datos proporcionada por la dependencia get_db().

    Usa:
        get_diagnosis_by_id_controller(): Función que consulta el diagnóstico en la base de datos.

    Roles requeridos:
        admin, medic

    Returns:
        db_diagnosis: Datos del diagnóstico solicitado o un error HTTP 400 si ocurre una excepción.
    """
    try:
        db_diagnosis = get_diagnosis_by_id_controller(id_diagnosis, db)
        return db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put(
    "/update/{id_diagnosis}", dependencies=[Depends(require_role(["admin", "medic"]))]
)
def update_diagnosis(
    id_diagnosis: str, update_info: DiagnosisUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza los datos de un diagnóstico existente.

    Args:
        id_diagnosis (str): Identificador único del diagnóstico a actualizar.
        update_info (DiagnosisUpdate): Datos nuevos del diagnóstico.
        db (Session): Sesión de base de datos proporcionada por la dependencia get_db().

    Usa:
        update_diagnosis_controller(): Función que actualiza el diagnóstico en la base de datos.

    Roles requeridos:
        admin, medic

    Returns:
        db_diagnosis: Objeto actualizado del diagnóstico o un error HTTP 400 si ocurre una excepción.
    """

    try:
        db_diagnosis = update_diagnosis_controller(id_diagnosis, update_info, db)
        return db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.delete(
    "/delete/{id_diagnosis}", dependencies=[Depends(require_role(["admin", "medic"]))]
)
def delete_diagnosis(id_diagnosis: str, db: Session = Depends(get_db)):
    """
    Elimina un diagnóstico existente por su ID.

    Args:
        id_diagnosis (str): Identificador único del diagnóstico a eliminar.
        db (Session): Sesión de base de datos proporcionada por la dependencia get_db().

    Usa:
        delete_diagnosis_controller(): Función que elimina el diagnóstico en la base de datos.

    Roles requeridos:
        admin, medic

    Returns:
        JSONResponse: Confirmación de eliminación o un error HTTP 400 si ocurre una excepción.
    """
    try:
        response = delete_diagnosis_controller(id_diagnosis, db)

        if not response:
            ValueError("Algo salio mal")
        return JSONResponse(
            content={"Response": response}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
