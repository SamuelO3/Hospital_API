from datetime import datetime
import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "User"

    id_user = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    rol_user = Column(String(60), nullable=False, default="User")
    active = Column(Boolean, default=True, nullable=False)

    # Relaciones
    user_information = relationship("UserInformation", back_populates="user")

    # Campos de auditoría
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), index=True, nullable=True
    )
    id_usuario_actualizacion = Column(
        UUID(as_uuid=True), ForeignKey("User.id_user"), index=True, nullable=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, index=True, nullable=True)
