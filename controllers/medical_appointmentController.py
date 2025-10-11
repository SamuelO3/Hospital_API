from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
# from models.medical_appointment import MedicalAppointment
from schemas.medical_appointment_schema import MedicalAppointmentCreate
from models.medical_appointment import MedicalAppointment as MedicalAppointment_model
from schemas.medical_appointment_schema import MedicalAppointment as MedicalAppointment_schema




def create_medical_appointment(db: Session, medical_appointment: MedicalAppointment_schema):
    """
    Crea una nueva cita médica en la base de datos.

    Args:
        db: Sesión de la base de datos
        medical_appointment: Información de la cita médica

    Returns:
        new_appointment: Cita médica creada en la db
    """
    try:
        new_appointment = MedicalAppointment_model(
            appointment_date=medical_appointment.appointment_date,
            appointment_hour=medical_appointment.appointment_hour,
            location=medical_appointment.location,
            id_medic=medical_appointment.id_medic,
            id_nurse=medical_appointment.id_nurse,
            id_patient=medical_appointment.id_patient,
            id_diagnosis=medical_appointment.id_diagnosis,
        )

        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



def get_medical_appointment_by_id(db: Session, appointment_id: UUID):
    """
    Obtiene una cita médica por su ID.

    Args:
        db: Sesión de la base de datos
        appointment_id: ID de la cita médica

    Returns:
        appointment: Cita médica encontrada en la db
    """
    appointment = db.query(MedicalAppointment_model).filter(
        MedicalAppointment_model.id_medical_appointment == appointment_id
    ).first()
    
    if appointment:
        return appointment
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cita médica con id '{appointment_id}' no encontrada"
        )


def get_all_medical_appointments(db: Session):
    """
    Obtiene todas las citas médicas en la base de datos.

    Args:
        db: Sesión de la base de datos

    Returns:
        appointments: Lista de citas médicas en la db
    """
    try:
        appointments = db.query(MedicalAppointment_model).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    if appointments:
        return appointments
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontraron citas médicas"
        )


def update_medical_appointment(db: Session, appointment_id: UUID, medical_appointment: MedicalAppointmentCreate):
    """
    Actualiza una cita médica en la base de datos.

    Args:
        db: Sesión de la base de datos
        appointment_id: ID de la cita médica
        medical_appointment: Información actualizada de la cita médica

    Returns:
        appointment_to_update: Cita médica actualizada en la db
    """
    try:
        appointment_to_update = get_medical_appointment_by_id(db, appointment_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    if appointment_to_update:
        try:
            appointment_to_update.appointment_date = medical_appointment.appointment_date
            appointment_to_update.appointment_hour = medical_appointment.appointment_hour
            appointment_to_update.location = medical_appointment.location
            appointment_to_update.id_medic = medical_appointment.id_medic
            appointment_to_update.id_nurse = medical_appointment.id_nurse
            appointment_to_update.id_patient = medical_appointment.id_patient
            appointment_to_update.id_diagnosis = medical_appointment.id_diagnosis
            
            db.commit()
            db.refresh(appointment_to_update)
            return appointment_to_update
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cita médica con id '{appointment_id}' no encontrada"
        )


def delete_medical_appointment(db: Session, appointment_id: UUID):
    """
    Elimina una cita médica de la base de datos.

    Args:
        db: Sesión de la base de datos
        appointment_id: ID de la cita médica

    Returns:
        appointment_to_delete: Cita médica eliminada de la db
    """
    try:
        appointment_to_delete = get_medical_appointment_by_id(db, appointment_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    if appointment_to_delete:
        try:
            db.delete(appointment_to_delete)
            db.commit()
            return appointment_to_delete
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cita médica con id '{appointment_id}' no encontrada"
        )