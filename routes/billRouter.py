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


router = APIRouter(prefix="/bill", tags=["Bills"])


@router.post("/", dependencies=[Depends(require_role(["admin", "nurse"]))])
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    try:
        db_bill = create_bill_controller(bill, db)
        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/all", dependencies=[Depends(require_role(["admin", "nurse"]))])
def get_all_bills(skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    try:
        list_db_bill = get_all_bills_controller(db, skip, limit)

        if not list_db_bill:
            raise ValueError("No existen facturas en la db")
        return list_db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/{id_bill}", dependencies=[Depends(require_role(["admin", "nurse"]))])
def get_bill(id_bill: str, db: Session = Depends(get_db)):
    try:
        db_bill = get_bill_by_id_controller(id_bill, db)

        if not db_bill:
            raise ValueError("No existe factura en la db")

        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put(
    "/update/{id_bill}", dependencies=[Depends(require_role(["admin", "nurse"]))]
)
def update_bill(id_bill: str, update_info: BillUpdate, db: Session = Depends(get_db)):
    try:
        db_bill = update_bill_controller(id_bill, update_info, db)

        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST0, detail=e)


@router.delete(
    "/delete/{id_bill}", dependencies=[Depends(require_role(["admin", "nurse"]))]
)
def delete_bill(id_bill: str, db: Session = Depends(get_db)):
    try:
        response = delete_bill_controller(id_bill, db)

        if not response:
            ValueError("Algo salio mal")

        return JSONResponse(
            content={"Response": response}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
