import uuid

from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class MedicalAppointment(Base):
    __tablename__ = "Medical_Appointment"

    id_medical_appointment = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    appointment_date = Column(Date, nullable=False)
    appointment_hour = Column(Time, nullable=False)
    location = Column(String(100), nullable=False)

    # Columnas con id de relaciones
    id_medic = Column(UUID(as_uuid=True), ForeignKey("Medic.id_medic"))
    id_nurse = Column(UUID(as_uuid=True), ForeignKey("Nurse.id_nurse"))
    id_patient = Column(UUID(as_uuid=True), ForeignKey("Patient.id_patient"))
    id_diagnosis = Column(UUID(as_uuid=True), ForeignKey("Diagnosis.id_diagnosis"))

    # relaciones
    bill = relationship("Bill", back_populates="medical_appointment")
    diagnosis = relationship("Diagnosis", back_populates="medical_appointment")
    medic = relationship("Medic", back_populates="appointment")
    nurse = relationship("Nurse", back_populates="appointment")
    patient = relationship("Patient", back_populates="appointment")

    # Campos Auditorias
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    id_user_create = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False
    )
    id_user_update = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=True
    )
