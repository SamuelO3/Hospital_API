from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class NurseBase(BaseModel):
    """
    Schema de enfermera con informacion base
    """

    speciality: str
    id_user_information: UUID

    class Config:
        orm_mode = True


    # first_name_user: str
    # second_name_user: Optional[str]
    # first_last_name_user: str
    # second_last_name_user: Optional[str]
    # birth_date_user: date
    # gender: str
    # phone_number: str
    # document_number: str
    # rol_user: str


class NurseCreate(NurseBase):
    """
    Schema de enfermera para crear una nueva enfermera
    """

    pass


class NurseResponse(NurseBase):
    """
    Schema de enfermera response
    """

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None
    creation_date: datetime
    id_user_create: UUID

    class Config:
        from_attributes = True


class Nurse(NurseBase):
    """
    Schema de enfermera con informacino basica de enfermera
    """

    id_nurse: UUID

# class NurseUpdate(BaseModel):
#     speciality: Optional[str] = None
#     id_user_information: Optional[UUID] = None


class NurseUpdate(BaseModel):
    speciality: Optional[str] = None
    id_user_information: Optional[UUID] = None

