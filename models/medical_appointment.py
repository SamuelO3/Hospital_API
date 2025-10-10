import uuid
from sqlalchemy import Column, Date, Time, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base


class MedicalAppointment(Base):
    __tablename__ = "Medical_Appointment"

    id_medical_appointment = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    appointment_date = Column(Date, nullable=False)
    appointment_hour = Column(Time, nullable=False)
    location = Column(String(100), nullable=False)

    id_medic = Column(UUID(as_uuid=True), ForeignKey("Medic.id_medic"), nullable=False)
    id_nurse = Column(UUID(as_uuid=True), ForeignKey("Nurse.id_nurse"), nullable=False)
    id_patient = Column(
        UUID(as_uuid=True), ForeignKey("Patient.id_patient"), nullable=False
    )
    id_diagnosis = Column(
        UUID(as_uuid=True), ForeignKey("Diagnosis.id_diagnosis"), nullable=False
    )

    # Relaciones
    medic = relationship("Medic", back_populates="appointments")
    nurse = relationship("Nurse", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    diagnosis = relationship("Diagnosis", back_populates="appointment")

    # Relación
    bill = relationship("Bill", back_populates="medical_appointment", uselist=False)

    # Auditoría
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
