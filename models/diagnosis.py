import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Diagnosis(Base):
    __tablename__ = "Diagnosis"

    id_diagnosis = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    diagnosis_date = Column(Date, nullable=False)
    diagnosis_description = Column(String(255), nullable=False)

    # columnas con IDs de relaciones
    id_medical_appointment = Column(
        UUID(as_uuid=True), ForeignKey("Medical_Appointment.id_medical_appointment")
    )

    # Relaciones
    medical_appointment = relationship("MedicalAppointment", back_populates="diagnosis")

    # Campos auditorias
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    id_user_create = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False
    )
    id_user_update = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=True
    )
