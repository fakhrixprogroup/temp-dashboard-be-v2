from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.schemas.auth_schema import AuthLogin, AuthLoginOut, AuthRegister, AuthRegisterOut
from app.schemas.sys_schema import BaseResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import AuthService
from app.utils.sys import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login", response_model=BaseResponse[AuthLoginOut])
async def login(
    data: AuthLogin,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        result = await service.login(data)
        return BaseResponse(
            message="Berhasil login",
            data=result
        )
    except Exception as e:
        print(f"Error login : {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error login : {e}",
                data=None
            ).model_dump()
        )

@router.post("/register", response_model=BaseResponse[AuthRegisterOut])
async def register(
    data: AuthRegister,
    db: AsyncSession = Depends(get_db)
):
    try:
        service = AuthService(db)
        result = await service.register(data)
        return BaseResponse(
            status="Success",
            message="Berhasil register",
            data=result
        )
    except Exception as e:
        print(f"Error register : {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error register : {e}",
                data=None
            ).model_dump()
        )