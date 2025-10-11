from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class DiagnosisBase(BaseModel):
    """
    Schema de diagnostico con informacion base
    """

    diagnosis_description: str


class DiagnosisCreate(DiagnosisBase):
    """
    Schema de diagnostico para crear un nuevo diagnostico
    """

    diagnosis_date: datetime


class DiagnosisUpdate(DiagnosisBase):
    """
    Schema de diagnostico para crear un nuevo diagnostico
    """

    pass


class DiagnosisResponse(DiagnosisBase):
    """
    Schema de diagnostico Response
    """

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None
    id_user_create: UUID
    creation_date: datetime

    class config:
        from_attributes = True


class Diagnosis(DiagnosisBase):
    """
    Schema de diagnostico con informacion basica
    """

    id_diagnosis: UUID
