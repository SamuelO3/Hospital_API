from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class MedicBase(BaseModel):
    """
    Schema de medico con informacino base
    """

    speciality: str

    first_name_user: str
    second_name_user: Optional[str]
    first_last_name_user: str
    second_last_name_user: Optional[str]
    birth_date_user: date
    gender: str
    phone_number: str
    document_number: str
    rol_user: str


class MedicCreate(MedicBase):
    """
    Schema de medico para crear nuevo medico
    """

    pass


class MedicResponse(MedicBase):
    """
    Schema de medico response
    """

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None
    id_user_create: UUID
    creation_date: datetime

    class Config:
        from_attributes = True


class Medic(MedicBase):
    """
    Schema de medico con informacino basica de medico
    """

    id_hospital_worker: UUID
