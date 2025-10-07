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


class User(UserBase):
    id_user: UUID
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id_usuario: UUID
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    activo: bool = True
