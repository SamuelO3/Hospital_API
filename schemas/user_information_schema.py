from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class UserInformationBase(BaseModel):
    first_name_user: str
    second_name_user: Optional[str] = None
    first_lastname_user: str
    second_lastname_user: Optional[str] = None
    birth_date_user: datetime
    gender_user: str
    phone_number_user: str
    document_number_user: str


class UserInformationCreate(UserInformationBase):
    rol_user: str
    id_user_creation: UUID


class UserInformationUpdate(UserInformationBase):
    id_user_update: Optional[UUID] = None


class UserInformation(UserInformationBase):
    id_user_information: UUID

    class Config:
        orm_mode = True
