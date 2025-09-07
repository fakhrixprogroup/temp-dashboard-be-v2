from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy import Enum, String
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RoleEnum(str, enum.Enum):
    admin = "admin"
    brand = "brand"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.admin)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    products = relationship("Product", back_populates="user", lazy="selectin")
    customers = relationship("Customer", back_populates="user", lazy="selectin")
    orders = relationship("Order", back_populates="user", lazy="selectin")