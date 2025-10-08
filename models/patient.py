import uuid

from database.config import Base

from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Patient(Base):
    __tablename__ = "Patient"

    id_patient = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )

    # Columnas con IDs de relaciones
    id_information = Column(
        UUID(as_uuid=True), ForeignKey("User_Information.id_user_information")
    )
    patient_information = relationship("UserInformation", back_populates="patient")

    # relaciones
    bill = relationship("Bill", back_populates="patient")
    patient_information = relationship("UserInformation", back_populates="patient")
    appointment = relationship("MedicalAppointment", back_populates="patient")

    # columnas  Auditorias
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    id_user_create = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False
    )
    id_user_update = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=True
    )
