import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base


class Nurse(Base):
    __tablename__ = "Nurse"

    id_nurse = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    speciality = Column(String(100), nullable=False)

    id_user_information = Column(
        UUID(as_uuid=True),
        ForeignKey("User_Information.id_user_information", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    nurse_information = relationship(
        "UserInformation", back_populates="nurse", passive_deletes=True
    )
    appointments = relationship(
        "MedicalAppointment",
        back_populates="nurse",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
