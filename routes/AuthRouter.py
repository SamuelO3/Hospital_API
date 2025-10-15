from typing import Union
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from controllers.user_information_controller import create_user_information

from database.config import get_db, SessionLocal

from controllers.auth_controller import create_user, autheticate_user, create_token_user

from schemas.user_information_schema import (
    UserInformationCreate,
    UserInformationResponse,
)
from schemas.user_schema import UserCreate, UserResponse, UserCreate
from schemas.auth_schema import LoginRequest, LoginResponse


router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")






@router.post("/login")
async def login(login: LoginRequest, db: SessionLocal = Depends(get_db)):
    try:
        user = autheticate_user(db, login.email, login.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # access_token_expires = timedelta(minutes=ACCES_TOKEN_EXPIRES_TIME)
        access_token = create_token_user(user)
        """
        Endpoint que autentica a un usuario y genera un token de acceso JWT.

        Args:
            login: Credenciales del usuario (correo electrónico y contraseña).
            db: Sesión de base de datos.

        Usa:
            autheticate_user: Función que valida las credenciales del usuario.
            create_token_user: Función que genera el token JWT para el usuario autenticado.

        Roles permitidos:
            Público (no requiere autenticación previa).

        Returns:
            LoginResponse: Objeto que contiene el token de acceso, su tipo y la información básica del usuario autenticado.
        """
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id_user=user.id_user,
                username=user.username,
                email=user.email,
                rol_user=user.rol_user,
                active=user.active,
            ),
        )
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    # user = get_user(form_data.username, db)
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    # if not verify_password(form_data.password, user.password):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    # access_token_expires = timedelta(minutes=ACCES_TOKEN_EXPIRES_TIME)
    # access_token = create_token_user(user)
    # return {"access_token": access_token, "token_type": "bearer"}





@router.post("/register")
async def register(
    user: UserCreate,
    user_information: UserInformationCreate,
    db: SessionLocal = Depends(get_db),
) -> JSONResponse:

    try:
        db_user = create_user(db, user)
        user_information.id_user = db_user.id_user
        db_user_information = create_user_information(db, user_information)

        """
        Endpoint que registra un nuevo usuario y su información asociada en la base de datos.

        Args:
            user: Datos de autenticación del usuario (credenciales y rol).
            user_information: Datos personales del usuario (información adicional).
            db: Sesión de base de datos.

        Usa:
            create_user: Función que registra al usuario en la base de datos.
            create_user_information: Función que guarda la información personal del usuario.

        Roles permitidos:
            Público (no requiere autenticación previa).

        Returns:
            UserResponse, db_user_information: Objetos con la información del usuario y su información asociada creados exitosamente.
        """
        return UserResponse.from_orm(db_user), db_user_information

    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    # if db.query(User).filter(User.email == user.email).first():
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')

    # db_user = User(
    #     username=user.username,
    #     email=user.email,
    #     password=get_hashed_password(user.password)
    # )
    # db.add(db_user)
    # db.commit()
    # return {"message": "User registered successfully"}

