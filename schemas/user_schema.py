from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id_user: UUID
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
