import uuid

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Bill(Base):
    __tablename__ = "Bill"

    id_bill = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    generation_date = Column(Date, nullable=False)
    generation_hour = Column(Time, nullable=False)
    total = Column(Float(precision=10), nullable=False)

    id_patient = Column(
        UUID(as_uuid=True), ForeignKey("Patient.id_patient"), nullable=False
    )
    id_medical_appointment = Column(
        UUID(as_uuid=True),
        ForeignKey("Medical_Appointment.id_medical_appointment"),
        unique=True,
        nullable=False,
    )

    # Relaciones
    medical_appointment = relationship("MedicalAppointment", back_populates="bill")

    # Auditoría
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    id_user_create = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False
    )
    id_user_update = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=True
    )
