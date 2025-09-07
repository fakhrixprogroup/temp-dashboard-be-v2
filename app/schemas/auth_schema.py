from typing import Optional
from pydantic import UUID4, BaseModel, EmailStr

from app.schemas.sys_schema import RoleEnum


class AuthRegisterBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: RoleEnum

class AuthRegister(AuthRegisterBase):
    pass

class AuthRegisterOut(AuthRegisterBase):
    id: UUID4

class AuthLogin(BaseModel):
    email: EmailStr
    password: str

class AuthLoginOut(BaseModel):
    id: UUID4
    accessToken: str
    token_type: str
    role: RoleEnum