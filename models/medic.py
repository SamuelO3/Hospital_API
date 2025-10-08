import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base


class Medic(Base):
    __tablename__ = "Medic"

    id_medic = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    specialty = Column(String(100), nullable=False)

    id_user_information = Column(
        UUID(as_uuid=True),
        ForeignKey("User_Information.id_user_information"),
        nullable=False,
    )

    # Relación
    medic_information = relationship("UserInformation", back_populates="medic")
    appointments = relationship("MedicalAppointment", back_populates="medic")

    # Auditoría
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    update_date = Column(DateTime(timezone=True), onupdate=func.now())
