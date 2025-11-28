from datetime import datetime
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.patient import Patient as Patient_model

from schemas.patient_schema import PatientCreate, PatientUpdate


def create_patient(db: Session, patient: PatientCreate):
    """
    Crea un nuevo paciente en la db

    Args:
        db: Sesion de la db
        patient: informacion del paciente

    return:
        db_patient: Informacion de paciente guardada en la db
    """

    try:
        db_patient = Patient_model(
            id_patient=uuid4(),
            id_user_information=patient.id_user_information,
            blood_type=patient.blood_type,
        )

        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

        return db_patient
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def get_patient_by_id(db: Session, id_patient: str):
    """
    Obtiene un paciente de la db mediante el id

    Args:
        db: Sesion de la db
        id_patient: id del paciente

    return:
        db_patient: Informacion de paciente guardada en la db
    """

    try:
        patient_uuid = UUID(id_patient) if isinstance(id_patient, str) else id_patient

        db_patient = (
            db.query(Patient_model)
            .filter(Patient_model.id_patient == patient_uuid)
            .first()
        )

        if not db_patient:
            raise ValueError("No existe el paciente en la db")

        return db_patient

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def get_all_patient(db: Session, limit: int = 15, skip: int = 0):
    """
    Obtiene todos los pacientes de la db paginados

    Args:
        db: Sesion de la db
        id_patient: id del paciente

    return:
        db_patient: Informacion de todos los pacientes guardados en la db (paginado)
    """
    try:
        list_db_patient = db.query(Patient_model).offset(skip).limit(limit).all()

        if not list_db_patient:
            raise ValueError("No existen pacientes en la db")
        return list_db_patient

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def update_patient(id_patient: str, update_info: PatientUpdate, db: Session):
    """
    Actualiza un paciente de la db mediante id

    Args:
        db: Sesion de la db
        id_patient: id del paciente a actualizar
        update_info: informacion del paciente a actualizar

    return:
        db_patient: Informacion de paciente guardada y actualizada en la db
    """

    try:
        db_patient = get_patient_by_id(db, id_patient)

        if not db_patient:
            raise ValueError("El paciente no existe")

        db_patient.update_date = datetime.now()
        db_patient.blood_type = update_info.blood_type

        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

        return db_patient

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def delete_patient(id_patient: str, db: Session) -> str:
    """
    Elimina un paciente de la db paginados

    Args:
        db: Sesion de la db
        id_patient: id del paciente a eliminar

    return:
        str: si el paciente fue eliminado correctamente
    """

    try:
        patient_to_delete = get_patient_by_id(db, id_patient)

        if not patient_to_delete:
            raise ValueError("No existe paciente para eliminar")

        db.delete(patient_to_delete)
        db.commit()

        return "Eliminado correctamente"

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
