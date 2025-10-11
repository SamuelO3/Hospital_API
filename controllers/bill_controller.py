from datetime import date, datetime, time

from fastapi import HTTPException, status
from models.bill import Bill as Bill_model

from sqlalchemy.orm import Session
from schemas.bill_schema import BillCreate, BillUpdate


def create_bill(bill: BillCreate, db: Session):
    """
    Crea una nueva factura en la db

    Args:
        db: Sesion de la db
        bill: informacion de la factura

    return:
        db_bill: Informacion de la factura guardada en la db
    """

    try:
        db_bill = Bill_model(
            generation_date=date.today(),
            generation_hour=datetime.now().time(),
            total=bill.total,
            id_patient=bill.id_patient,
            id_medical_appointment=bill.id_medical_appointment,
        )

        db.add(db_bill)
        db.commit()
        db.refresh(db_bill)

        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def get_bill_by_id(id_bill: str, db: Session):
    """
    Obtiene una factura de la db mediante su id.

    Args:
        db: Sesion de la db
        id_bill: ID de la factura a buscar

    return:
        db_bill: Informacion de la factura guardada en la db
    """

    try:

        db_bill = db.query(Bill_model).filter(Bill_model.id_bill == id_bill).first()

        if not db_bill:
            raise ValueError("No existe la factura en la db")

        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def get_all_bills(db: Session, skip: int = 0, limit: int = 15):
    """
    Obtiene todas las facturas de la db.

    Args:
        db: Sesion de la db

    return:
        list_db_bill: Informacion de la factura guardada en la db
    """

    try:

        list_db_bill = db.query(Bill_model).offset(skip).limit(limit).all()

        if not list_db_bill:
            raise ValueError("No existe la factura en la db")

        return list_db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def update_bill(id_bill: str, update_info: BillUpdate, db: Session):
    """
    Actualiza una factura mediante el id.

    Args:
        db: Sesion de la db
        id_bill: ID de la factura a actualizar
        update_info: informacion para actualizar la factura

    return:
        db_bill: Informacion de la factura actualizada y guardada en la db
    """

    try:

        db_bill = get_bill_by_id(id_bill, db)

        if not db_bill:
            raise ValueError("No existe la factura en la db")

        db_bill.total = update_info.total
        db_bill.update_date = datetime.now()

        db.commit()
        db.refresh(db_bill)

        return db_bill
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def delete_bill(id_bill: str, db: Session) -> str:
    """
    elimina una factura mediante el ID.

    Args:
        db: Sesion de la db

    return:
        str: Si la factura se elimino correctamente
    """
    try:
        bill_to_delete = get_bill_by_id(id_bill, db)

        if not bill_to_delete:
            raise ValueError("No existe factura en la db")

        db.delete(bill_to_delete)
        db.commit()

        return "Eliminado exitosamente"

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
