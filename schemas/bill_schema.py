from datetime import datetime, date, time
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class BillBase(BaseModel):
    """
    Schema de factura con informacion base
    """

    total: float


class BillCreate(BillBase):
    """
    Schema de factura para crear una nueva factura
    """

    generation_date: date
    generation_hour: time

    id_patient: str
    id_medical_appointment: str


class BillUpdate(BillBase):
    """
    Schema de factura para actualizar una factura
    """

    pass


class BillRespone(BillBase):
    """
    Schema de factura Response
    """

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None
    creation_date: datetime
    id_user_create: UUID

    class config:
        from_attributes = True


class Bill(BillBase):
    """
    Schema de factura con informacion basica de factura
    """

    id_bill: UUID
