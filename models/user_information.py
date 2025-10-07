import uuid

from database.config import Base

from sqlalchemy import Column, ForeignKey, String, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class UserInformation(Base):
    __tablename__ = "User_Information"

    id_user_information = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    first_name_user = Column(String(50), nullable=False)
    second_name_user = Column(String(50), nullable=True)
    first_lastname_user = Column(String(50), nullable=False)
    second_lastname_user = Column(String(50), nullable=True)

    birth_date_user = Column(Date, nullable=False)
    gender_user = Column(String(50), nullable=False)
    phone_number_user = Column(String(20), nullable=False)
    document_number_user = Column(String(30), nullable=False)

    # Columnas con IDs de relaciones
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id_user"))

    # Relaciones para back_populates
    medic = relationship("Medic", back_populates="medic_information")
    patient = relationship("Patient", back_populates="patient_information")
    nurse = relationship("Nurse", back_populates="nurse_information")
    user = relationship("User", back_populates="user_information")

    # Columnas Auditorias
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
    id_user_create = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False
    )
    id_user_update = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=True
    )
