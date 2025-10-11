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
