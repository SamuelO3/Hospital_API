from fastapi import FastAPI
from routes import AuthRouter, MedicRouter, diagnosisRouter, patientRouter
from database.config import get_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Sistema de Gestión Médica",
    description="API para la gestion hospitalaria.",
    version="1.2.0",
    openapi_tags=[
        {
            "name": "Patient",
            "description": "Operaciones relacionadas con el manejo de pacientes.",
        },
        {"name": "Medic", "description": "Gestión de información de médicos."},
        {"name": "Nurse", "description": "Gestion de información de enfermeras."},
        {
            "name": "Medical appointment",
            "description": "Agendamiento y consulta de citas médicas.",
        },
        {
            "name": "Diagnosis",
            "description": "Registro y consulta de diagnósticos médicos.",
        },
        {"name": "Bill", "description": "Gestión de facturación y pagos."},
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
get_db()
