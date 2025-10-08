from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth.JWTHandler import (
    create_access_token,
    decode_access_token,
    ACCES_TOKEN_EXPIRES_TIME,
)
from auth.security import get_hashed_password, verify_password
from controllers.auth_controller import create_user, autheticate_user, create_token_user
from schemas.auth_schema import LoginRequest, UserCreate, UserResponse, LoginResponse
from schemas.user_schema import UserBase

from models.user import User
from database.config import get_db, SessionLocal
from schemas.user_schema import UserCreate, User, UserBase

from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user(mail: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.email == mail).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return user


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/login")
async def login(login: LoginRequest, db: SessionLocal = Depends(get_db)):
    try:
        user = autheticate_user(db, login.username, login.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCES_TOKEN_EXPIRES_TIME)
        access_token = create_token_user(user)
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
async def register(user: UserCreate, db: SessionLocal = Depends(get_db)):

    try:
        db_user = create_user(db, user)
        return UserResponse.from_orm(db_user)
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
