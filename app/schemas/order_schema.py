from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field

from app.schemas.auth_schema import AuthRegisterBase


class OrderItemBase(BaseModel):
    product_name: str = Field(..., description="Product name")
    order_qty: int = Field(..., gt=0, description="Order quantity (must be positive)")
    file_url: Optional[str]


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    product_name: Optional[str] = Field(None, description="Product name")
    order_qty: Optional[int] = Field(None, gt=0, description="Order quantity (must be positive)")
    file_url: Optional[str]


class OrderItemResponse(OrderItemBase):
    id: UUID4 = Field(..., description="Order item ID")
    order_id: UUID4 = Field(..., description="Associated order ID")

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    order_reference_number: str = Field(..., description="Order reference number")
    issues_date: datetime = Field(..., description="Order issue date")
    due_date: datetime = Field(..., description="Order due date")
    name: str = Field(..., max_length=255, description="Customer name")
    address: str = Field(..., max_length=255, description="Customer address")
    receiver_name: str = Field(..., max_length=255, description="Receiver name")
    address_2: Optional[str]
    suburb: Optional[str]
    state: Optional[str]
    post_code: Optional[str]
    phone_number: Optional[str]


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate] = Field(default=[], description="List of order items")


class OrderUpdate(BaseModel):
    order_reference_number: Optional[str] = Field(None, description="Order reference number")
    issues_date: Optional[datetime] = Field(None, description="Order issue date")
    due_date: Optional[datetime] = Field(None, description="Order due date")
    name: Optional[str] = Field(None, max_length=255, description="Customer name")
    address: Optional[str] = Field(None, max_length=255, description="Customer address")
    receiver_name: Optional[str] = Field(None, max_length=255, description="Receiver name")
    address_2: Optional[str]
    suburb: Optional[str]
    state: Optional[str]
    phone_number: Optional[str]
    post_code: Optional[str]
    order_items: List[OrderItemCreate] = Field(default=[], description="List of order items")


class OrderResponse(OrderBase):
    id: UUID4 = Field(..., description="Order ID")
    user_id: UUID4 = Field(..., description="User ID associated with the order")
    created_at: datetime = Field(..., description="Order creation timestamp")

    class Config:
        from_attributes = True


class OrderUserOut(BaseModel):
    first_name: str
    last_name: str
    role: str
    
    class Config:
        from_attributes = True


class OrderWithItemsResponse(OrderResponse):
    order_id: str
    user: Optional["OrderUserOut"] = None
    order_items: List[OrderItemResponse] = Field(default=[], description="List of order items")