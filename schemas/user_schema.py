from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re


class UserBase(BaseModel):
    username: str = Field(..., min_length=4)
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def password_validator(cls, v):
        """
        Valida que la contraseña tenga al menos una mayúscula, un número
        y mínimo 8 caracteres.
        """
        # Al menos una mayúscula, al menos un número, mínimo 8 caracteres en total
        pattern = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "La contraseña debe tener minimo una mayuscula y un numero"
            )
        return v


class User(UserBase):
    id_user: str
    created_at: datetime
    updated_at: datetime
