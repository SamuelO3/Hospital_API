"""
Modulo para manejar el Token de JWT
"""

from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta, timezone

import os
from dotenv import load_dotenv

load_dotenv("./config/.env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGOTIHM")
ACCES_TOKEN_EXPIRES_TIME = os.getenv("ACCES_TOKEN_EXPIRES_TIME")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Crea un token seguro para el JWT

    args:
        data: datos del usuario en JSON
        expires_delta: cuanto debe durar el token

    return:
        cadena de texto que representa el token de jwt
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCES_TOKEN_EXPIRES_TIME)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    decodifica el token jwt previamente creado

    args:
        token: token previametne creado

    return
        payload: con los claims del diccionario del token

    raises:
        Exceptin si el token es invalido o expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid Token")
