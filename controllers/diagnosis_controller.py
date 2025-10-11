from datetime import date, datetime
from uuid import uuid4
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.diagnosis import Diagnosis as Diagnosis_model
from schemas.diagnosis_schema import DiagnosisCreate, DiagnosisUpdate


def create_diagnosis(diagnosis: DiagnosisCreate, db: Session):
    """
    Crea un nuvo diagnostico en la db

    Args:
        diagnosis: informacion del diagnostico
        db: Sesion de la db

    return:
        db_diagnosis: Informacion del diagnostico guardada en la db
    """

    try:
        db_diagnosis = Diagnosis_model(
            id_diagnosis=uuid4(),
            diagnosis_description=diagnosis.diagnosis_description,
            diagnosis_date=date.today(),
        )

        db.add(db_diagnosis)
        db.commit()
        db.refresh(db_diagnosis)

        return db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def get_diagnosis_by_id(id_diagnosis: str, db: Session):
    """
    Obtiene un diagnostico mediante el id

    Args:
        id_diagnosis: ID del diagnostico
        db: Sesion de la db

    return:
        db_diagnosis: Informacion del diagnostico guardada en la db
    """
    try:
        db_diagnosis = (
            db.query(Diagnosis_model)
            .filter(Diagnosis_model.id_diagnosis == id_diagnosis)
            .first()
        )
        if not db_diagnosis:
            raise ValueError("No existe el diagnostico en la db")

        return db_diagnosis

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def get_all_diagnosis(db: Session, skip: int = 0, limit: int = 15):
    """
    Obtiene diagnosticos de la db paginados

    Args:
        db: Sesion de la db
        skip: numero de registros a saletar
        limit: numero de registros limite

    return:
        list_db_diagnosis: lista de diagnosticos de la db
    """

    try:
        list_db_diagnosis = db.query(Diagnosis_model).offset(skip).limit(limit).all()

        if not list_db_diagnosis:
            raise ValueError("No hay diagnosticos en la db")

        return list_db_diagnosis

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def update_diagnosis(id_diagnosis: str, update_info: DiagnosisUpdate, db: Session):
    """
    Actualiza un diagnostico de la db mediante su id

    Args:
        id_diagnosis: ID del diagnostico a actualizar
        update_info: informacino para actualizar el diagnostico
        db: Sesion de la db

    return:
        db_diagnosis: diagnostico actualizado
    """

    try:
        db_diagnosis = get_diagnosis_by_id(id_diagnosis, db)

        if not db_diagnosis:
            raise ValueError("No existe el diganostico en la db")

        db_diagnosis.diagnosis_description = update_info.diagnosis_description
        db_diagnosis.update_date = datetime.now()

        db.commit()
        db.refresh(db_diagnosis)

        return db_diagnosis

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


def delete_diagnosis(id_diagnosis: str, db: Session) -> str:
    """
    elimina un diagnostico de la db mediante su id

    Args:
        id_diagnosis: ID del diagnostico a actualizar
        db: Sesion de la db

    return:
        True: si la eliminacion fue correcta
    """

    try:
        diagnosis_to_delete = get_diagnosis_by_id(id_diagnosis, db)

        if not diagnosis_to_delete:
            raise ValueError("No existe diagnositico para eliminar")

        db.delete(diagnosis_to_delete)
        db.commit()

        return "Eliminado correctamente"

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
