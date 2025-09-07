from datetime import datetime
from typing import Optional
from pydantic import UUID4, BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")


class ProductResponse(ProductBase):
    id: UUID4 = Field(..., description="Product ID")
    user_id: UUID4 = Field(..., description="User ID who created the product")
    created_at: datetime = Field(..., description="Product creation timestamp")

    class Config:
        from_attributes = True