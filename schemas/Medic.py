from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class HospitalWorkerBase(BaseModel):
    speciality: str


class HospitalWorkerCreate(HospitalWorkerBase):
    id_user_create: UUID
    creation_date: datetime


class HospitalWorker(HospitalWorkerBase):
    id_hospital_worker: UUID

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None

    class Config:
        orm_mode = True
