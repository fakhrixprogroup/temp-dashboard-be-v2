from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from datetime import datetime
import uuid

from app.models.customer_models import Customer
from app.models.order_models import Order, OrderItem, generate_order_id
from app.models.product_models import Product
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.schemas.sys_schema import TokenData
from sqlalchemy.orm import selectinload


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: OrderCreate, user: TokenData) -> Order:
        try:
            # Debug logging for dates
            print(f"Debug - Issues date: {order_data.issues_date} (type: {type(order_data.issues_date)})")
            print(f"Debug - Due date: {order_data.due_date} (type: {type(order_data.due_date)})")
            
            # Validate dates
            # if order_data.due_date <= order_data.issues_date:
            #     raise ValueError(f"Due date ({order_data.due_date}) must be after issues date ({order_data.issues_date})")

            customer = (await self.db.execute(
                select(Customer)
                .where(
                    Customer.name.ilike(order_data.name),
                )
            )).scalar_one_or_none()

            if not customer:
                customer = Customer(
                    user_id=user.user_id,
                    name=order_data.name,
                    address=order_data.address,
                    receiver_name=order_data.receiver_name,
                    address_2=order_data.address_2,
                    suburb=order_data.suburb,
                    state=order_data.state,
                    phone_number=order_data.phone_number,
                    post_code=order_data.post_code
                )
                self.db.add(customer)
                await self.db.flush()
            else:
                if customer.address != order_data.address:
                    customer.address = order_data.address
                if customer.receiver_name != order_data.receiver_name:
                    customer.receiver_name = order_data.receiver_name
                if customer.address_2 != order_data.address_2:
                    customer.address_2 = order_data.address_2
                if customer.suburb != order_data.suburb:
                    customer.suburb = order_data.suburb
                if customer.state != order_data.state:
                    customer.state = order_data.state
                if customer.phone_number != order_data.phone_number:
                    customer.phone_number = order_data.phone_number
                if customer.post_code != order_data.post_code:
                    customer.post_code = order_data.post_code
                await self.db.commit()
                await self.db.refresh(customer)

            # Generate order_id
            order_id = await generate_order_id(self.db)
            
            # Create main order
            db_order = Order(
                user_id=user.user_id,
                order_id=order_id,
                order_reference_number=order_data.order_reference_number,
                issues_date=order_data.issues_date,
                due_date=order_data.due_date,
                name=order_data.name,
                address=order_data.address,
                address_2=order_data.address_2,
                suburb=order_data.suburb,
                state=order_data.state,
                receiver_name=order_data.receiver_name,
                post_code=order_data.post_code,
                phone_number=order_data.phone_number
            )
            
            self.db.add(db_order)
            await self.db.flush()  # Flush to get the order ID
            
            # Create order items if provided
            if order_data.order_items:
                for item_data in order_data.order_items:
                    product = (await self.db.execute(
                        select(Product)
                        .where(Product.name.ilike())
                    ))
                    if product is None:
                        product_model = Product(
                            name=item_data.product_name
                        )
                        self.db.add(product_model)
                        await self.db.flush()
                        
                    db_order_item = OrderItem(
                        order_id=db_order.id,
                        product_name=item_data.product_name,
                        order_qty=item_data.order_qty,
                        file_url=item_data.file_url
                    )
                    self.db.add(db_order_item)
            
            await self.db.commit()
            await self.db.refresh(db_order)
            
            return db_order
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error creating order: {e}")

    async def get_orders(self, user: TokenData, skip: int = 0, limit: int = 100) -> List[Order]:
        try:
            query = select(Order).where(Order.user_id == user.user_id).options(selectinload(Order.user)).offset(skip).limit(limit)
            result = await self.db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            raise Exception(f"Error getting orders: {e}")

    async def get_order_by_id(self, order_id: uuid.UUID, user: TokenData) -> Optional[Order]:
        try:
            query = select(Order).where(Order.id == order_id, Order.user_id == user.user_id)
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
            
        except Exception as e:
            raise Exception(f"Error getting order: {e}")

    async def update_order(self, order_id: uuid.UUID, order_data: OrderUpdate, user: TokenData) -> Optional[Order]:
        try:
            # Get existing order
            db_order = await self.get_order_by_id(order_id, user)
            if not db_order:
                return None
            
            # Update fields
            # if order_data.order_reference_number is not None:
            #     db_order.order_reference_number = order_data.order_reference_number
            # if order_data.issues_date is not None:
            #     db_order.issues_date = order_data.issues_date
            # if order_data.due_date is not None:
            #     db_order.due_date = order_data.due_date
            # if order_data.name is not None:
            #     db_order.name = order_data.name
            # if order_data.address is not None:
            #     db_order.address = order_data.address
            # if order_data.receiver_name is not None:
            #     db_order.receiver_name = order_data.receiver_name
            
            # Validate dates if both are provided
            # if db_order.due_date <= db_order.issues_date:
            #     raise ValueError("Due date must be after issues date")

            customer = (await self.db.execute(
                select(Customer)
                .where(
                    Customer.name.ilike(order_data.name),
                )
            )).scalar_one_or_none()

            if not customer:
                customer = Customer(
                    user_id=user.user_id,
                    name=order_data.name,
                    address=order_data.address,
                    receiver_name=order_data.receiver_name,
                    address_2=order_data.address_2,
                    suburb=order_data.suburb,
                    state=order_data.state,
                    phone_number=order_data.phone_number,
                    post_code=order_data.post_code
                )
                self.db.add(customer)
                await self.db.flush()
            else:
                if customer.address != order_data.address:
                    customer.address = order_data.address
                if customer.receiver_name != order_data.receiver_name:
                    customer.receiver_name = order_data.receiver_name
                if customer.address_2 != order_data.address_2:
                    customer.address_2 = order_data.address_2
                if customer.suburb != order_data.suburb:
                    customer.suburb = order_data.suburb
                if customer.state != order_data.state:
                    customer.state = order_data.state
                if customer.phone_number != order_data.phone_number:
                    customer.phone_number = order_data.phone_number
                if customer.post_code != order_data.post_code:
                    customer.post_code = order_data.post_code
                await self.db.commit()
                await self.db.refresh(customer)

            
            await self.db.commit()
            await self.db.refresh(db_order)

            await self.db.execute(
                delete(OrderItem).where(OrderItem.order_id == db_order.id)
            )
            await self.db.commit()

            if order_data.order_items:
                for item_data in order_data.order_items:
                    db_order_item = OrderItem(
                        order_id=db_order.id,
                        product_name=item_data.product_name,
                        order_qty=item_data.order_qty,
                        file_url=item_data.file_url
                    )
                    self.db.add(db_order_item)
            
            await self.db.commit()
            await self.db.refresh(db_order)
            
            return db_order
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error updating order: {e}")

    async def delete_order(self, order_id: uuid.UUID, user: TokenData) -> bool:
        try:
            # Get existing order
            db_order = await self.get_order_by_id(order_id, user)
            if not db_order:
                return False
            
            await self.db.delete(db_order)
            await self.db.commit()
            
            return True
            
        except Exception as e:
            await self.db.rollback()
            raise Exception(f"Error deleting order: {e}")