from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

from schemas.user_schema import UserResponse

"""
    Schemas para auth
"""


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[UUID] = None
    rol: Optional[str] = None
