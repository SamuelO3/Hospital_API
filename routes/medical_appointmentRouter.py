from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from database.config import get_db
from controllers.medical_appointmentController import (
    create_medical_appointment,
    get_medical_appointment_by_id,
    get_all_medical_appointments,
    update_medical_appointment,
    delete_medical_appointment,
)
from utils.role_utils import require_role

from schemas.medical_appointment_schema import (
    MedicalAppointment as MedicalAppointment_schema,
)
from schemas.medical_appointment_schema import MedicalAppointmentCreate

# from models.medical_appointment import MedicalAppointment

router = APIRouter(prefix="/medical_appointment", tags=["Medical Appointments"])


@router.get(
    "/{id_medical_appointment}",
    dependencies=[Depends(require_role(["admin", "medic"]))],
)
def get_medical_appointment_by_id_route(
    id_medical_appointment: UUID, db: Session = Depends(get_db)
):
    """
    Obtiene una cita médica por su ID.

    Roles permitidos: admin, medic
    """
    return get_medical_appointment_by_id(db, id_medical_appointment)


@router.post("/", dependencies=[Depends(require_role(["admin", "medic"]))])
def create_medical_appointment_route(
    medical_appointment: MedicalAppointmentCreate, db: Session = Depends(get_db)
):
    """
    Crea una nueva cita médica en la base de datos.

    Roles permitidos: admin, medic
    """

    db_medical_appointment = create_medical_appointment(db, medical_appointment)
    return


@router.get("/", dependencies=[Depends(require_role(["admin", "medic"]))])
def get_all_medical_appointments_route(db: Session = Depends(get_db)):
    """
    Obtiene todas las citas médicas en la base de datos.
    """
    return get_all_medical_appointments(db)


@router.put(
    "/{id_medical_appointment}",
    dependencies=[Depends(require_role(["admin", "medic"]))],
)
def update_medical_appointment_route(
    id_medical_appointment: UUID,
    medical_appointment: MedicalAppointment_schema,
    db: Session = Depends(get_db),
):
    """
    Actualiza una cita médica en la base de datos.

    Roles permitidos: admin, medic
    """
    return update_medical_appointment(db, id_medical_appointment, medical_appointment)


@router.delete(
    "/{id_medical_appointment}",
    dependencies=[Depends(require_role(["admin", "medic"]))],
)
def delete_medical_appointment_route(
    id_medical_appointment: UUID, db: Session = Depends(get_db)
):
    """
    Elimina una cita médica de la base de datos.

    Roles permitidos: admin, medic
    """
    return delete_medical_appointment(db, id_medical_appointment)
