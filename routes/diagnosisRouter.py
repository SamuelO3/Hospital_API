from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.config import get_db
from utils.role_utils import require_role

from controllers.diagnosis_controller import (
    create_diagnosis as create_diagnosis_controller,
    get_all_diagnosis as get_all_diagnosis_controller,
    get_diagnosis_by_id as get_diagnosis_by_id_controller,
    update_diagnosis as update_diagnosis_controller,
    delete_diagnosis as delete_diagnosis_controller,
)
from schemas.diagnosis_schema import DiagnosisCreate, DiagnosisUpdate


router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])


@router.post("/", dependencies=[Depends(require_role(["admin", "medic"]))])
def create_diagnosis(diagnosis: DiagnosisCreate, db: Session = Depends(get_db)):
    try:
        db_diagnosis = create_diagnosis_controller(diagnosis, db)

        return db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/all", dependencies=[Depends(require_role(["admin", "medic"]))])
def get_all_diagnosis(db: Session = Depends(get_db), skip: int = 0, limit: int = 15):
    try:
        list_db_diagnosis = get_all_diagnosis_controller(db, skip, limit)

        return list_db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.get("/{id_diagnosis}", dependencies=[Depends(require_role(["admin", "medic"]))])
def get_diagnosis(id_diagnosis: str, db: Session = Depends(get_db)):

    try:
        db_diagnosis = get_diagnosis_by_id_controller(id_diagnosis, db)

        return db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.put(
    "/update/{id_diagnosis}", dependencies=[Depends(require_role(["admin", "medic"]))]
)
def update_diagnosis(
    id_diagnosis: str, update_info: DiagnosisUpdate, db: Session = Depends(get_db)
):

    try:
        db_diagnosis = update_diagnosis_controller(id_diagnosis, update_info, db)

        return db_diagnosis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


@router.delete(
    "/delete/{id_diagnosis}", dependencies=[Depends(require_role(["admin", "medic"]))]
)
def delete_diagnosis(id_diagnosis: str, db: Session = Depends(get_db)):
    try:
        result = delete_diagnosis_controller(id_diagnosis, db)

        return JSONResponse(
            content={"Response": result}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
