from datetime import datetime
import uuid
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base


class UserInformation(Base):
    __tablename__ = "User_Information"

    id_user_information = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    first_name_user = Column(String(50), nullable=False)
    second_name_user = Column(String(50), nullable=True)
    first_lastname_user = Column(String(50), nullable=False)
    second_lastname_user = Column(String(50), nullable=True)
    birth_date_user = Column(Date, nullable=False)
    gender_user = Column(String(20), nullable=False)
    phone_number_user = Column(String(20), nullable=False)
    document_number_user = Column(String(30), nullable=False)

    id_user = Column(
        UUID(as_uuid=True),
        ForeignKey("User.id_user", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Relaciones
    medic = relationship(
        "Medic",
        back_populates="medic_information",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    patient = relationship(
        "Patient",
        back_populates="patient_information",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    nurse = relationship(
        "Nurse",
        back_populates="nurse_information",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # dentro de UserInformation
    user = relationship("User", back_populates="user_information", passive_deletes=True)

    # 🔹 Auditoría
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
