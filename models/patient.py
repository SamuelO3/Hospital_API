import uuid

from database.config import Base

from sqlalchemy import Column, ForeignKey, String, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import Relationship, relationship
from sqlalchemy.dialects.postgresql import UUID


class Patient(Base):
    __tablename__ = "Patient"

    id_patient = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )

    # relacion con tabla user_information

    id_information = Column(
        UUID(as_uuid=True), ForeignKey("User_Information.id_user_information")
    )
    patient_information = Relationship("UserInformation", back_populates="patient")

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
        overlaps="user,user_create,hospital_worker",
    )
    user_update = relationship(
        "User",
        foreign_keys=[id_user_update],
        overlaps="user,user_update,hospital_worker",
    )
