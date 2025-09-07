from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.models.customer_models import Customer
from app.schemas.customer_schema import CustomerCreate, CustomerUpdate
from app.schemas.sys_schema import TokenData


class CustomerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_customer(self, customer_data: CustomerCreate, user: TokenData) -> Customer:
        try:
            db_customer = Customer(
                user_id=user.user_id,
                name=customer_data.name,
                address=customer_data.address,
                receiver_name=customer_data.receiver_name,
                address_2=customer_data.address_2,
                suburb=customer_data.suburb,
                state=customer_data.state,
                phone_number=customer_data.phone_number,
                post_code=customer_data.post_code
            )
            
            self.db.add(db_customer)
            await self.db.commit()
            await self.db.refresh(db_customer)
            
            return db_customer
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error creating customer: {e}")

    async def get_customers(self, user: TokenData, skip: int = 0, limit: int = 100) -> List[Customer]:
        try:
            query = select(Customer).where(Customer.user_id == user.user_id).offset(skip).limit(limit)
            result = await self.db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            raise Exception(f"Error getting customers: {e}")

    async def get_customer_by_id(self, customer_id: uuid.UUID, user: TokenData) -> Optional[Customer]:
        try:
            query = select(Customer).where(Customer.id == customer_id, Customer.user_id == user.user_id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            raise Exception(f"Error getting customer: {e}")

    async def update_customer(self, customer_id: uuid.UUID, customer_data: CustomerUpdate, user: TokenData) -> Optional[Customer]:
        try:
            # Get existing customer
            db_customer = await self.get_customer_by_id(customer_id, user)
            if not db_customer:
                return None
            
            # Update fields
            if customer_data.name is not None:
                db_customer.name = customer_data.name
            if customer_data.address is not None:
                db_customer.address = customer_data.address
            if customer_data.receiver_name is not None:
                db_customer.receiver_name = customer_data.receiver_name
            
            await self.db.commit()
            await self.db.refresh(db_customer)
            
            return db_customer
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error updating customer: {e}")

    async def delete_customer(self, customer_id: uuid.UUID, user: TokenData) -> bool:
        try:
            # Get existing customer
            db_customer = await self.get_customer_by_id(customer_id, user)
            if not db_customer:
                return False
            
            await self.db.delete(db_customer)
            await self.db.commit()
            
            return True
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error deleting customer: {e}")