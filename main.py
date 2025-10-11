from fastapi import FastAPI

from routes import AuthRouter, MedicRouter, NurseRouter, UserRouter

from routes import AuthRouter, MedicRouter, patientRouter, MedicalAppointmentRouter

from database.config import engine, Base, get_db
from routes import AuthRouter, MedicRouter, diagnosisRouter, patientRouter
from database.config import get_db
from fastapi.middleware.cors import CORSMiddleware


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

app.include_router(patientRouter.router)
app.include_router(diagnosisRouter.router)
get_db()

app.include_router(UserRouter.router)
get_db()

app.include_router(MedicalAppointmentRouter.router)
get_db()