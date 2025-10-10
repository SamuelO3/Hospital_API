import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base


class User(Base):
    __tablename__ = "User"

    id_user = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    rol_user = Column(String(60), nullable=False)
    active = Column(Boolean, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relación con UserInformation
    user_information = relationship(
        "UserInformation", back_populates="user", uselist=False
    )
