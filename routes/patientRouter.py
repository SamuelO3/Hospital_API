from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database.config import get_db
from schemas.patient_schema import Patient, PatientCreate, PatientUpdate
from utils.role_utils import require_role

from controllers.patient_controller import (
    create_patient as create_patient_controller,
    get_all_patient,
    get_patient_by_id,
    update_patient as update_patient_controller,
    delete_patient as delete_patient_controller,
)


router = APIRouter(prefix="/patient", tags=["Patients"])


@router.post("/", dependencies=[Depends(require_role(["user", "admin"]))])
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):

    try:
        db_patient = create_patient_controller(db, patient)
        """
    Endpoint que crea un nuevo registro de paciente en la base de datos.

    Args:
        patient: Datos del paciente a registrar.
        db: Sesión de base de datos.

    Usa:
        create_patient_controller: Función que registra un nuevo paciente en la base de datos.

    Roles permitidos:
        user, admin

    Returns:
        db_patient: Objeto con la información del paciente creado.
    """

        return db_patient
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/all",
    response_model=List[Patient],
    dependencies=[Depends(require_role("admin"))],
)
def get_patients(skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):

    try:
        db_patients = get_all_patient(db, limit=limit, skip=skip)
        """
        Endpoint que obtiene todos los pacientes registrados en la base de datos.

        Args:
            skip: Número de registros a omitir para la paginación.
            limit: Número máximo de registros a devolver.
            db: Sesión de base de datos.

        Usa:
            get_all_patient: Función que consulta todos los pacientes registrados.

        Roles permitidos:
            admin

        Returns:
            db_patient: Lista de pacientes registrados en la base de datos.
        """


        return db_patients
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{id_patient}", dependencies=[Depends(require_role(["user", "medic", "admin"]))]
)
def get_patient(id_patient: str, db: Session = Depends(get_db)):

    try:
        db_patient = get_patient_by_id(db, id_patient)
        """
        Endpoint que obtiene la información de un paciente específico por su ID.

        Args:
            id_patient: Identificador único del paciente.
            db: Sesión de base de datos.

        Usa:
            get_patient_by_id: Función que consulta el paciente en la base de datos.

        Roles permitidos:
            user, medic, admin

        Returns:
            db_patient: Datos del paciente correspondiente al ID proporcionado.
        """


        return db_patient
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put(
    "/update/{id_patient}",
    dependencies=[Depends(require_role(["user", "admin", "medic"]))],
)
def update_patient(
    id_patient: str, update_info: PatientUpdate, db: Session = Depends(get_db)
):
    try:
        db_patient = update_patient_controller(id_patient, update_info, db)
        """
        Endpoint que actualiza la información de un paciente existente en la base de datos.

        Args:
            id_patient: Identificador único del paciente a actualizar.
            update_info: Datos actualizados del paciente.
            db: Sesión de base de datos.

        Usa:
            update_patient_controller: Función que actualiza la información del paciente en la base de datos.

        Roles permitidos:
            user, admin, medic

        Returns:
            db_patient: Objeto con la información actualizada del paciente.
        """

        return db_patient
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/delete/{id_patient}",
    dependencies=[Depends(require_role(["user", "admin"]))],
)
def delete_patient(id_patient: str, db: Session = Depends(get_db)):

    try:
        response = delete_patient_controller(id_patient, db)

        if not response:
            ValueError("Algo salio mal")
            """
            Endpoint que elimina un paciente existente de la base de datos.

            Args:
                id_patient: Identificador único del paciente a eliminar.
                db: Sesión de base de datos.

            Usa:
                delete_patient_controller: Función que elimina el registro del paciente en la base de datos.

            Roles permitidos:
                user, admin

            Returns:
                delete_patient_controller: Confirmación de eliminación del paciente.
            """

        return JSONResponse(
            content={"Response": response}, status_code=status.HTTP_200_OK
        )
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
