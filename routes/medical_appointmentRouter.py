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
    Descripcion:
        Obtiene una cita médica específica de la base de datos mediante su ID.

    Args:
        id_medical_appointment (UUID): Identificador único de la cita médica.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        get_medical_appointment_by_id(db, id_medical_appointment)

    Returns:
        MedicalAppointment: Objeto con los datos de la cita médica encontrada.
    """
    return get_medical_appointment_by_id(db, id_medical_appointment)


@router.post(
    "/",
    response_model=MedicalAppointment_schema,
    dependencies=[Depends(require_role(["admin", "medic"]))],
)
def create_medical_appointment_route(
    medical_appointment: MedicalAppointmentCreate, db: Session = Depends(get_db)
):
    """
    Descripcion:
        Crea una nueva cita médica y la guarda en la base de datos.

    Args:
        medical_appointment (MedicalAppointmentCreate): Datos de la cita médica a registrar.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        create_medical_appointment(db, medical_appointment)

    Returns:
        MedicalAppointment: Objeto con la información de la cita médica creada.
    """
    db_medical_appointment = create_medical_appointment(db, medical_appointment)
    return db_medical_appointment


@router.get(
    "/all/",
    response_model=list[MedicalAppointment_schema],
    dependencies=[Depends(require_role(["admin", "medic"]))],
)
def get_all_medical_appointments_route(db: Session = Depends(get_db)):
    """
    Descripcion:
        Obtiene todas las citas médicas registradas en la base de datos.

    Args:
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        get_all_medical_appointments(db)

    Returns:
        list[MedicalAppointment]: Lista con todas las citas médicas almacenadas.
    """
    return get_all_medical_appointments(db)


@router.put(
    "/{id_medical_appointment}",
    dependencies=[Depends(require_role(["admin", "medic"]))],
)
def update_medical_appointment_route(
    id_medical_appointment: UUID,
    medical_appointment: MedicalAppointmentCreate,
    db: Session = Depends(get_db),
):
    """
    Descripcion:
        Actualiza la información de una cita médica existente en la base de datos.

    Args:
        id_medical_appointment (UUID): Identificador de la cita médica a actualizar.
        medical_appointment (MedicalAppointmentCreate): Nuevos datos de la cita médica.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        update_medical_appointment(db, id_medical_appointment, medical_appointment)

    Returns:
        MedicalAppointment: Objeto con la cita médica actualizada.
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
    Descripcion:
        Elimina una cita médica existente en la base de datos mediante su ID.

    Args:
        id_medical_appointment (UUID): Identificador único de la cita médica a eliminar.
        db (Session): Sesión de base de datos inyectada por dependencia.

    Usa:
        delete_medical_appointment(db, id_medical_appointment)

    Returns:
        dict: Mensaje de confirmación o resultado de la eliminación.
    """
    return delete_medical_appointment(db, id_medical_appointment)
