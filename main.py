from fastapi import FastAPI
from routes import AuthRouter, MedicRouter, NurseRouter
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
app.include_router(MedicRouter.router)
app.include_router(NurseRouter.router)
get_db()