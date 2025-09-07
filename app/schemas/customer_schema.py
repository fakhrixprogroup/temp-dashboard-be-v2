from typing import Optional
from pydantic import UUID4, BaseModel, Field

from app.schemas.auth_schema import AuthRegisterOut


class CustomerBase(BaseModel):
    name: str = Field(..., max_length=255, description="Customer name")
    phone_number: str = Field(..., description="Customer phone number")
    address: str = Field(..., max_length=255, description="Customer address")
    receiver_name: Optional[str] = Field(None, description="Receiver name")
    address_2: Optional[str]
    suburb: Optional[str]
    state: Optional[str]
    post_code: Optional[str]


class CustomerCreate(CustomerBase):
    user_id: UUID4 = Field(..., description="User ID associated with the customer")


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Customer name")
    address: Optional[str] = Field(None, max_length=255, description="Customer address")
    receiver_name: Optional[str] = Field(None, description="Receiver name")
    user_id: Optional[UUID4] = Field(None, description="User ID associated with the customer")


class CustomerResponse(CustomerBase):
    id: UUID4 = Field(..., description="Customer ID")
    user_id: UUID4 = Field(..., description="User ID associated with the customer")

    class Config:
        from_attributes = True


class CustomerWithUserResponse(CustomerResponse):
    user: Optional[AuthRegisterOut] = Field(None, description="Associated user information")