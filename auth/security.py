"""
Modulo de seguridad para manejo de contraseñas
"""

import bcrypt


def get_hashed_password(password: str) -> str:
    """
    Genera un hash seguro de una contraseña

    args:
        password: contraseña plana

    return:
        hash de la contraseña con salt
    """

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password=password.encode("utf-8"), salt=salt)

    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    verifica que las contraseñas  coincidan

    args:
        password: contraseña plana
        hashed_password: hash almacenado

    return:
        True si la contraseña es correcta, False si la contraseña es incorrecta.
    """
    result = bcrypt.checkpw(
        password=plain_password.encode("uft-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )
    return result
