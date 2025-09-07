import uuid
from sqlalchemy import UUID, ForeignKey, String, Text
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    phone_number: Mapped[str]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    address_2: Mapped[str] = mapped_column(Text, nullable=True)
    suburb: Mapped[str] = mapped_column(String(255), nullable=True)
    state: Mapped[str] = mapped_column(String(255), nullable=True)
    receiver_name: Mapped[str] = mapped_column(String(255), nullable=True)
    post_code: Mapped[str] = mapped_column(nullable=True)

    user = relationship("User", back_populates="customers", lazy="selectin")