from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from controllers.bill_controller import (
    create_bill as create_bill_controller,
    get_bill_by_id as get_bill_by_id_controller,
    get_all_bills as get_all_bills_controller,
    update_bill as update_bill_controller,
    delete_bill as delete_bill_controller,
)

from database.config import get_db
from schemas.bill_schema import BillCreate, BillUpdate
from utils.role_utils import require_role

from models.bill import Bill

router = APIRouter(prefix="/bill", tags=["Bills"])


@router.post(
    "/", dependencies=[Depends(require_role(["admin", "nurse"]))], response_model=Bill
)
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    """
    EndPoint para crear una nueva factura en el sistema.

    Args:
        bill: Datos de la factura a registrar.
        db: Sesión de db

    Usa:
        create_bill_controller: Función encargada de registrar la factura en la base de datos.

    Roles requeridos:
        admin, nurse

    Returns:
        Bill: Objeto con la información de la factura creada o un error HTTP 400 si ocurre una excepción.
    """
    try:
        db_bill = create_bill_controller(bill, db)
        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get(
    "/all",
    dependencies=[Depends(require_role(["admin", "nurse"]))],
    response_model=list[Bill],
)
def get_all_bills(skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    """
    EndPoint para obtener una lista de todas las facturas registradas.

    Args:
        skip: Número de registros a omitir para la paginación. Por defecto 0.
        limit: Número máximo de registros a devolver. Por defecto 15.
        db: Sesión de base de datos

    Usa:
        get_all_bills_controller: Función que consulta todas las facturas.

    Roles requeridos:
        admin, nurse

    Returns:
        list_db_bill: Lista de facturas registradas o un error HTTP 400 si ocurre una excepción.
    """
    try:
        list_db_bill = get_all_bills_controller(db, skip, limit)
        if not list_db_bill:
            raise ValueError("No existen facturas en la db")
        return list_db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get(
    "/{id_bill}",
    dependencies=[Depends(require_role(["admin", "nurse"]))],
    response_model=Bill,
)
def get_bill(id_bill: str, db: Session = Depends(get_db)):
    """
    EndPoint para obtener la información de una factura específica por su ID.

    Args:
        id_bill: Identificador de la factura.
        db: Sesión de base de datos.

    Usa:
        get_bill_by_id_controller: Función que consulta una factura en la base de datos.

    Roles requeridos:
        admin, nurse

    Returns:
        db_bill: Datos de la factura solicitada o un error HTTP 400 si ocurre una excepción.
    """
    try:
        db_bill = get_bill_by_id_controller(id_bill, db)

        if not db_bill:
            raise ValueError("No existe factura en la db")
        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put(
    "/update/{id_bill}",
    dependencies=[Depends(require_role(["admin", "nurse"]))],
    response_model=Bill,
)
def update_bill(id_bill: str, update_info: BillUpdate, db: Session = Depends(get_db)):
    """
    EndPoint que actualiza la información de una factura existente.

    Args:
        id_bill: Identificador de la factura a actualizar.
        update_info: Datos nuevos para la factura.
        db : Sesión de base de datos.

    Usa:
        update_bill_controller: Función que aplica los cambios en la base de datos.

    Roles requeridos:
        admin, nurse

    Returns:
        db_bill: Objeto actualizado de la factura o un error HTTP 400 si ocurre una excepción.
    """
    try:
        db_bill = update_bill_controller(id_bill, update_info, db)
        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST0, detail=e)


@router.delete(
    "/delete/{id_bill}",
    dependencies=[Depends(require_role(["admin", "nurse"]))],
    response_model=Bill,
)
def delete_bill(id_bill: str, db: Session = Depends(get_db)):
    """
    EndPoint elimina una factura existente por su ID.

    Args:
        id_bill: Identificador único de la factura a eliminar.
        db: Sesión de base de datos.

    Usa:
        delete_bill_controller: Función que elimina la factura en la base de datos.

    Roles requeridos:
        admin, nurse

    Returns:
        JSONResponse: Mensaje de confirmación de eliminación o un error HTTP 400 si ocurre una excepción.
    """
    try:
        response = delete_bill_controller(id_bill, db)

        if not response:
            ValueError("Algo salio mal")
        return JSONResponse(
            content={"Response": response}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
