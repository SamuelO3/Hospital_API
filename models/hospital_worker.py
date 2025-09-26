import uuid

from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from database.config import Base


class HospitalWorker(Base):
    __tablename__ = "Hospital_Worker"

    id_hospital_worker = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    speciality = Column(String(50), nullable=False)

    # Relacion con user_information
    id_information = Column(
        UUID(as_uuid=True),
        ForeignKey("User_Information.id_user_information"),
        nullable=False,
    )
    hospital_worker_information = relationship(
        "UserInformation", back_populates="hospital_worker"
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
        overlaps="user,user_create,hospital_worker",
    )
    user_update = relationship(
        "User",
        foreign_keys=[id_user_update],
        overlaps="user,user_update,hospital_worker",
    )
