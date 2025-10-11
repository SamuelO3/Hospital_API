from datetime import date, datetime, time
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class MedicalAppointmentBase(BaseModel):
    """
    Schema de cita medica con informacion base
    """

    appointment_date: date
    appointment_hour: time
    location: str
    id_medic: UUID
    id_nurse: UUID
    id_patient: UUID
    id_diagnosis: UUID


class MedicalAppointmentCreate(MedicalAppointmentBase):
    """
    Schema de cita medica para crear nueva cita medica
    """

    pass


class MedicalAppointmentResponse(MedicalAppointmentBase):
    """
    Schema de cita medica Response
    """

    update_date: Optional[datetime] = None
    id_user_update: Optional[UUID] = None
    creation_date: datetime
    id_user_create: UUID

    class config:
        from_attributes = True


class MedicalAppointment(MedicalAppointmentBase):
    """
    Schema de cita medica con informacion basica de cita medica
    """

    id_medical_appointment: UUID


# class MedicalAppointmentUpdate(BaseModel):
#     appointment_date: Optional[date] = None
#     appointment_hour: Optional[time] = None
#     location: Optional[str] = None
#     id_medic: Optional[UUID] = None
#     id_nurse: Optional[UUID] = None
#     id_patient: Optional[UUID] = None
#     id_diagnosis: Optional[UUID] = None