from fastapi import Depends, HTTPException, status
from auth.dependencies import get_current_user

def require_role(required_role: str):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role_user") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol '{required_role}'."
            )
        return current_user
    return role_checker
