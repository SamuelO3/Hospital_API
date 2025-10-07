import uuid

from sqlalchemy import Column, ForeignKey, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class Nurse(Base):
    __tablename__ = "Nurse"

    id_nurse = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    salary = Column(Float(15, 2), nullable=False)
    speciality = Column(String(50), nullable=False)

    # Columnas con IDs de relaciones
    id_information = Column(
        UUID(as_uuid=True), ForeignKey("User_Information.id_user_information")
    )

    # Relaciones
    nurse_information = relationship("UserInformation", back_populates="nurse")
    appointment = relationship("MedicalAppointment", back_populates="nurse")

    # Campos Auditorias
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    id_user_create = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False
    )
    id_user_update = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=True
    )
