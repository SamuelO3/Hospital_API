
from datetime import date, datetime
from uuid import uuid4
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.medical_appointment import MedicalAppointment as medicalappointmentmodel
from schemas.medical_appointment_schema import MedicalAppointmentCreate, MedicalAppointmentResponse, MedicalAppointmentBase
def create_medical_appointment(medicalappo: MedicalAppointmentCreate, db: Session):
    """
    Crea un nueva cita en la db

    Args:
        cita: informacion de la cita
        db: Sesion de la db

    return:
        db_cita: Informacion de la cita guardada en la db
    """

    try:
        db_medical_appointment = medicalappointmentmodel(
            id_medical_appointment=uuid4(),
            appointment_date = medicalappo.appointment_date ,
            appointment_hour=medicalappo.appointment_hour,
            location=medicalappo.location,
        )

        db.add(db_medical_appointment)
        db.commit()
        db.refresh(db_medical_appointment)

        return db_medical_appointment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def get_medical_appointment_by_id(id_medical_appointment: str, db: Session):
    """
    Obtiene una cita mediante el id

    Args:
        id_medical_appointments: ID de la cita
        db: Sesion de la db

    return:
        mapp_db: Informacion de la cita guardada en la db
    """
    mapp_db = db.query(medicalappointmentmodel).filter(medicalappointmentmodel.id_medical_appointment == id_medical_appointment).first()
    if mapp_db:
        return mapp_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"mapp with id '{id_medical_appointment}' not found")


def get_medical_appointment(db: Session):
    """
    Obtiene todos las citas en la base de datos.

    Args
        db:Sesion de la base de datos

    return:
        mapp: lista de citas en la db
    """
    mapp = db.query(medicalappointmentmodel).all()
    if mapp:
        return mapp
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron citas")


def update_medical_appointment(db: Session, id_medical_appointment: str, medicalappo: MedicalAppointmentBase):
    """
    Actualiza una cita en la base de datos.

    Args
        db:Sesion de la base de datos
        id_medical_appointment: id de la cita
        medicalappo: informacion de la cita

    return:
        medicalappo: cita actualizado en la db
    """
    medicalappo_to_update = get_medical_appointment_by_id(db, id_medical_appointment)
    if medicalappo_to_update:
        try:
            medicalappo_to_update.appointment_date = medicalappo.appointment_date
            medicalappo_to_update.appointment_hour = medicalappo.appointment_hour
            medicalappo_to_update.location = medicalappo.location
            db.commit()
            db.refresh( medicalappo_to_update)
            return  medicalappo_to_update
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise


def delete_medical_appointment(db: Session, id_medical_appointment: str):
    """
    Elimina una cita de la base de datos.

    Args
        db:Sesion de la base de datos
        id_medical_appointment: id de la cita

    return:
        medical_to_delete: cita eliminado de la db
    """
    medical_to_delete = get_medical_appointment_by_id(db, id_medical_appointment)
    if  medical_to_delete:
        try:
            db.delete( medical_to_delete)
            db.commit()
            return  medical_to_delete
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise 
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
        return new_appointment

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
            
            diagnosis = appointment_to_delete.diagnosis
            if diagnosis:
                db.delete(diagnosis)
                db.delete(appointment_to_delete)
            else:
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
