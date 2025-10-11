from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class PatientBase(BaseModel):
    """
    Schema de paciente con informacion base
    """

    pass
    # first_name_user: str
    # second_name_user: Optional[str]
    # first_last_name_user: str
    # second_last_name_user: Optional[str]
    # birth_date_user: date
    # gender: str
    # phone_number: str
    # document_number: str
    # rol_user: str
    blood_type: str


class PatientCreate(PatientBase):
    """
    Schema de paciente para crear un nuevo paciente
    """

    id_user_information: str
    pass


class PatientUpdate(PatientBase):
    """
    Schema de paciente para Actualizar un paciente
    """

    pass


class PatientResponse(PatientBase):
    """
    Schema para respuesta de paciente
    """

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None
    creation_date: datetime
    id_user_create: UUID

    class Config:
        from_attributes = True


class Patient(PatientBase):
    """
    Schema con toda la informacion de basica de paciente
    """

    id_patient: UUID
