from fastapi import APIRouter, HTTPException, Depends
from auth.JWTHandler import create_access_token, decode_access_token, ACCES_TOKEN_EXPIRES_TIME
from models.user import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.config import get_db, SessionLocal
from schemas.user_schema import UserCreate, User, UserBase
from models.user import User
from auth.security import get_hashed_password, verify_password
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_user(mail: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.email == mail).first()
    if not user:
        raise HTTPException(status_code=404, detail='Not Found')
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = get_user(form_data.username, db)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(user: UserCreate, db: SessionLocal = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail='Email already registered')

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_hashed_password(user.password)
    )        
    db.add(db_user)
    db.commit()
    return {"message": "User registered successfully"}

