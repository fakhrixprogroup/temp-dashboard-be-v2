from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_models import User
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth_schema import AuthLogin, AuthRegister
from passlib.context import CryptContext

from app.utils.sys import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthRepository(db)

    async def login(self, data: AuthLogin):
        user = await self.repo.get_by_email(data)
        if not user:
            return None
        
        if not pwd_context.verify(data.password, user.password):
            return None
        
        token = create_access_token(data={"sub":str(user.id), "role": user.role})
        if not token:
            return None

        return {
            "role": user.role,
            "accessToken": str(token),
            "token_type": "Bearer",
            "id": user.id
        }

    async def register(self, data: AuthRegister):
        try:
            hashed = pwd_context.hash(data.password)
            user = User(**data.dict(exclude={"password"}), password=hashed)
            result = await self.repo.register(user)

            return result
        except Exception as e:
            print(f"Error register : {e}")
            raise e