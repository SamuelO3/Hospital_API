import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base


class Patient(Base):
    __tablename__ = "Patient"

    id_patient = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    blood_type = Column(String(10), nullable=False, index=True)

    id_user_information = Column(
        UUID(as_uuid=True),
        ForeignKey("User_Information.id_user_information", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    patient_information = relationship(
        "UserInformation", back_populates="patient", passive_deletes=True
    )
    appointments = relationship(
        "MedicalAppointment",
        back_populates="patient",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
