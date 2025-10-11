from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

"""
    Schemas de User
"""


class UserBase(BaseModel):
    username: str
    email: EmailStr
    rol_user: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr] = None
    rol_user: Optional[str]
    password: Optional[str]
    activo: Optional[bool] = True
    updated_at: Optional[datetime] = None


class User(UserBase):
    id_user: UUID
    activo: bool = True


class UserResponse(UserBase):
    id_user: UUID
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
