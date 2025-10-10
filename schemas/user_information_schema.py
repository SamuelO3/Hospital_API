from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

#! Posiblemente este schema no tenga ningun uso


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
    pass


class UserInformationUpdate(UserInformationBase):
    pass


class UserInformationResponse(UserInformationBase):
    id_user_creation: UUID
    id_user_update: Optional[UUID] = None
    creation_date: datetime
    update_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserInformation(UserInformationBase):
    id_user_information: UUID
