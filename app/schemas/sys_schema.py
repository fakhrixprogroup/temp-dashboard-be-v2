from decimal import Decimal
import enum
from typing import Generic, TypeVar
from pydantic import UUID4, BaseModel, ConfigDict

T = TypeVar("T")

class RoleEnum(str, enum.Enum):
    admin = "admin"
    brand = "brand"

class BaseResponse(BaseModel, Generic[T]):
    status: str = "Success"
    message: str
    data: T | None = None

class TokenData(BaseModel):
    user_id: UUID4
    # role: RoleEnum

class SysConfigurationBase(BaseModel):
    key: str
    value_in_persen: Decimal
    is_active: bool

class SysConfigurationOut(SysConfigurationBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4

class MasterPaymentMethodBase(BaseModel):
    name: str
    code: str
    is_active: bool

class MasterPaymentMethodCreate(MasterPaymentMethodBase):
    pass

class MasterPaymentMethodOut(MasterPaymentMethodBase):
    id: UUID4
