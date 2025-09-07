from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_models import User
from app.schemas.auth_schema import AuthLogin

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_email(self, data: AuthLogin):
        query = (
            select(User)
            .where(User.email == data.email)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def register(self, data: User):
        self.db.add(data)
        await self.db.commit()
        await self.db.refresh(data)
        return data
    
    async def get_by_id(self, id: UUID4):
        query = (
            select(User)
            .where(User.id == id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()