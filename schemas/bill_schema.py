from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class BillBase(BaseModel):
    """
    Schema de factura con informacion base
    """

    generation_date: date
    generation_hour: datetime.time
    total: float


class BillCreate(BillBase):
    """
    Schema de factura para crear una nueva factura
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


class Bill(BillBase):
    """
    Schema de factura con informacion basica de factura
    """

    id_bill: UUID

    class config:
        orm_mode = True
