from datetime import datetime, date
import uuid

from sqlalchemy import UUID, ForeignKey, String, Date, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    order_reference_number: Mapped[str] = mapped_column(String(255), nullable=False)
    issues_date: Mapped[datetime] = mapped_column(nullable=False)
    due_date: Mapped[datetime] = mapped_column(nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    address_2: Mapped[str] = mapped_column(nullable=True)
    suburb: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(nullable=True)
    receiver_name: Mapped[str] = mapped_column(nullable=True)
    post_code: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user = relationship("User", back_populates="orders", lazy="selectin")
    order_items = relationship("OrderItem", back_populates="order", lazy="selectin", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"))
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    order_qty: Mapped[int] = mapped_column(nullable=False)
    file_url: Mapped[str] = mapped_column(nullable=True)

    order = relationship("Order", back_populates="order_items", lazy="selectin")

class OrderSequence(Base):
    __tablename__ = "order_sequences"
    date: Mapped[date] = mapped_column(Date, primary_key=True)
    sequence_number: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

async def generate_order_id(db: AsyncSession) -> str:
    """Generate order_id dengan format DDMMYY-0000+n yang reset setiap hari"""
    today = date.today()
    
    # Cek apakah sudah ada sequence untuk hari ini
    result = await db.execute(
        select(OrderSequence).where(OrderSequence.date == today)
    )
    sequence_record = result.scalar_one_or_none()
    
    if sequence_record is None:
        # Buat record baru untuk hari ini
        sequence_record = OrderSequence(date=today, sequence_number=1)
        db.add(sequence_record)
    else:
        # Increment sequence yang sudah ada
        sequence_record.sequence_number += 1
    
    await db.flush()  # Pastikan perubahan tersimpan
    
    # Format: DDMMYY-0000+n
    date_str = today.strftime("%d%m%y")
    sequence_str = f"{sequence_record.sequence_number:04d}"
    
    return f"{date_str}-{sequence_str}"