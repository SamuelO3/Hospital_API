from fastapi import FastAPI
from routes import AuthRouter
from database.config import engine, Base, get_db
from fastapi.middleware.cors import CORSMiddleware
from database.config import create_tables

create_tables()


app = FastAPI()

cors = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(AuthRouter.router)

get_db()