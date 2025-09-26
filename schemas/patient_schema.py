from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class PatientBase(BaseModel):
    pass


class PatietnCreate(PatientBase):
    id_user_create: UUID
    creation_date: datetime


class Patient(PatientBase):
    id_patient: UUID

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None

    class Config:
        orm_mode = True
