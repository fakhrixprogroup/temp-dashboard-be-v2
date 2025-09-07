from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.models.product_models import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.schemas.sys_schema import TokenData


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_product(self, product_data: ProductCreate, user: TokenData) -> Product:
        try:
            db_product = Product(
                user_id=user.user_id,
                name=product_data.name,
                description=product_data.description
            )
            
            self.db.add(db_product)
            await self.db.commit()
            await self.db.refresh(db_product)
            
            return db_product
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error creating product: {e}")

    async def get_products(self, user: TokenData, skip: int = 0, limit: int = 100) -> List[Product]:
        try:
            query = select(Product).where(Product.user_id == user.user_id).offset(skip).limit(limit)
            result = await self.db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            raise Exception(f"Error getting products: {e}")

    async def get_product_by_id(self, product_id: uuid.UUID, user: TokenData) -> Optional[Product]:
        try:
            query = select(Product).where(Product.id == product_id, Product.user_id == user.user_id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            raise Exception(f"Error getting product: {e}")

    async def update_product(self, product_id: uuid.UUID, product_data: ProductUpdate, user: TokenData) -> Optional[Product]:
        try:
            # Get existing product
            db_product = await self.get_product_by_id(product_id, user)
            if not db_product:
                return None
            
            # Update fields
            if product_data.name is not None:
                db_product.name = product_data.name
            if product_data.description is not None:
                db_product.description = product_data.description
            
            await self.db.commit()
            await self.db.refresh(db_product)
            
            return db_product
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error updating product: {e}")

    async def delete_product(self, product_id: uuid.UUID, user: TokenData) -> bool:
        try:
            # Get existing product
            db_product = await self.get_product_by_id(product_id, user)
            if not db_product:
                return False
            
            await self.db.delete(db_product)
            await self.db.commit()
            
            return True
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error deleting product: {e}")