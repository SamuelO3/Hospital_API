from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, session
from auth.JWTHandler import verify_token

from schemas.user_information_schema import UserInformation as information

"""
    Metodos para crear, leer, actualizar y eliminar user_information
"""


def create_user_information(
    db: session, information: information, token: str = Depends()
):

    return
