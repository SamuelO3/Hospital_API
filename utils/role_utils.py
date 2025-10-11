from fastapi import Depends, HTTPException, status
from auth.dependencies import get_current_user
from typing import Union, List

def require_role(required_roles: Union[str, List[str]]):
    """
    Dependencia que valida si el usuario tiene alguno de los roles requeridos.
    
    Args:
        required_roles (str | list[str]): Rol o lista de roles permitidos.
    """
    if isinstance(required_roles, str):
        required_roles = [required_roles]  # Convertir a lista si es solo un string

    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role_user")

        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere alguno de los roles: {', '.join(required_roles)}."
            )
        return current_user

    return role_checker
