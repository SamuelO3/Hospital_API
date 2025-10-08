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
        ForeignKey("User_Information.id_user_information"),
        nullable=False,
    )

    nurse_information = relationship("UserInformation", back_populates="nurse")
    appointments = relationship("MedicalAppointment", back_populates="nurse")

    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
