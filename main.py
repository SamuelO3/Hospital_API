from fastapi import FastAPI
from routes import (
    AuthRouter,
    MedicRouter,
    billRouter,
    diagnosisRouter,
    patientRouter,
    medical_appointmentRouter,
)
from database.config import get_db, create_tables
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Sistema de Gestión Médica",
    description="API para la gestion hospitalaria.",
    version="1.2.0",
    openapi_tags=[
        {
            "name": "Patients",
            "description": "Operaciones relacionadas con el manejo de pacientes.",
        },
        {"name": "Medics", "description": "Gestión de información de médicos."},
        {"name": "Nurses", "description": "Gestion de información de enfermeras."},
        {
            "name": "Medical Appointments",
            "description": "Agendamiento y consulta de citas médicas.",
        },
        {
            "name": "Diagnosis",
            "description": "Registro y consulta de diagnósticos médicos.",
        },
        {"name": "Bills", "description": "Gestión de facturación y pagos."},
        {"name": "Auth", "description": "Gestión de login y registro."},
    ],
)


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
app.include_router(billRouter.router)
get_db()
