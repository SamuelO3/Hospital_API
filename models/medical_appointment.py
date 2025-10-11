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

    id_medic = Column(
        UUID(as_uuid=True),
        ForeignKey("Medic.id_medic", ondelete="CASCADE"),
        nullable=False,
    )
    id_nurse = Column(
        UUID(as_uuid=True),
        ForeignKey("Nurse.id_nurse", ondelete="CASCADE"),
        nullable=False,
    )
    id_patient = Column(
        UUID(as_uuid=True),
        ForeignKey("Patient.id_patient", ondelete="CASCADE"),
        nullable=False,
    )
    id_diagnosis = Column(
        UUID(as_uuid=True),
        ForeignKey("Diagnosis.id_diagnosis", ondelete="CASCADE"),
        nullable=False,
    )

    # Relaciones
    medic = relationship("Medic", back_populates="appointments", passive_deletes=True)
    nurse = relationship("Nurse", back_populates="appointments", passive_deletes=True)
    patient = relationship(
        "Patient", back_populates="appointments", passive_deletes=True
    )
    diagnosis = relationship(
        "Diagnosis", back_populates="appointment", passive_deletes=True
    )

    # Relación
    bill = relationship(
        "Bill",
        back_populates="medical_appointment",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Auditoría
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
