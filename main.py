from fastapi import FastAPI
from routes import AuthRouter, MedicRouter, diagnosisRouter, patientRouter, medical_appointmentRouter
from database.config import get_db, create_tables
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
create_tables()

cors = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(AuthRouter.router)
app.include_router(MedicRouter.router)
app.include_router(patientRouter.router)
app.include_router(diagnosisRouter.router)
app.include_router(medical_appointmentRouter.router)
get_db()
