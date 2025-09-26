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

    rol_user = Column(String(60), nullable=False)

    # Relaciones para back_populates
    hospital_worker = relationship(
        "HospitalWorker", back_populates="hospital_worker_information"
    )
    patient = relationship("Patient", back_populates="patient_information")

    # Relacion con tabla user
    user_id = Column(UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False)
    user = relationship(
        "User",  # -> nombre de la clase donde se creo el modelo objetivo
        back_populates="user_information",
        foreign_keys=[user_id],
    )

    # ID auditorias
    id_user_create = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=False
    )
    id_user_update = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), nullable=True
    )

    # Fechas Auditorias
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacions Auditorias
    user_create = relationship(
        "User",
        foreign_keys=[id_user_create],
        overlaps="user,user_create,user_information",
    )
    user_update = relationship(
        "User",
        foreign_keys=[id_user_update],
        overlaps="user,user_update,user_information",
    )
