from datetime import date, datetime
from uuid import UUID, uuid4
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
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


def get_diagnosis_by_id(id_diagnosis: str, db: Session):
    try:
        diagnosis_uuid = (
            UUID(id_diagnosis) if isinstance(id_diagnosis, str) else id_diagnosis
        )

        db_diagnosis = (
            db.query(Diagnosis_model)
            .filter(Diagnosis_model.id_diagnosis == diagnosis_uuid)
            .first()
        )

        if not db_diagnosis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existe el diagnostico en la db",
            )

        return db_diagnosis

    except HTTPException:
        raise
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="UUID inválido"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


def get_all_diagnosis(db: Session, skip: int = 0, limit: int = 15):
    try:
        list_db_diagnosis = db.query(Diagnosis_model).offset(skip).limit(limit).all()

        if not list_db_diagnosis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existen diagnosticos en la db",
            )

        return list_db_diagnosis

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def update_diagnosis(id_diagnosis: str, update_info: DiagnosisUpdate, db: Session):
    try:
        db_diagnosis = get_diagnosis_by_id(id_diagnosis, db)

        db_diagnosis.diagnosis_description = update_info.diagnosis_description

        if hasattr(update_info, "diagnosis_date") and update_info.diagnosis_date:
            db_diagnosis.diagnosis_date = update_info.diagnosis_date

        db_diagnosis.update_date = datetime.now()

        db.commit()
        db.refresh(db_diagnosis)

        return db_diagnosis

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def delete_diagnosis(id_diagnosis: str, db: Session) -> str:
    try:
        diagnosis_to_delete = get_diagnosis_by_id(id_diagnosis, db)

        db.delete(diagnosis_to_delete)
        db.commit()

        return "Eliminado correctamente"

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
