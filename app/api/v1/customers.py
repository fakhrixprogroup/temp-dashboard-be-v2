from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.schemas.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate
from app.schemas.sys_schema import BaseResponse, TokenData
from app.services.customer_service import CustomerService
from app.utils.sys import get_db, get_current_user


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get("/", response_model=BaseResponse[List[CustomerResponse]])
async def get_customers(
    skip: int = Query(0, ge=0, description="Number of customers to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of customers to return"),
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = CustomerService(db)
        customers = await service.get_customers(user, skip, limit)
        
        return BaseResponse(
            status="Success",
            message="Berhasil mengambil data customers",
            data=[CustomerResponse.model_validate(customer) for customer in customers]
        )
        
    except Exception as e:
        print(f"Error get customers: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error get customers: {e}",
                data=None
            ).model_dump()
        )


@router.get("/{customer_id}", response_model=BaseResponse[CustomerResponse])
async def get_customer_by_id(
    customer_id: UUID4,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = CustomerService(db)
        customer = await service.get_customer_by_id(customer_id, user)
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return BaseResponse(
            status="Success",
            message="Berhasil mengambil data customer",
            data=CustomerResponse.model_validate(customer)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error get customer: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error get customer: {e}",
                data=None
            ).model_dump()
        )


@router.post("/", response_model=BaseResponse[CustomerResponse])
async def create_customer(
    customer_data: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = CustomerService(db)
        result = await service.create_customer(customer_data, user)
        
        return BaseResponse(
            status="Success",
            message="Customer created successfully",
            data=CustomerResponse.model_validate(result)
        )
        
    except Exception as e:
        print(f"Error create customer: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error create customer: {e}",
                data=None
            ).model_dump()
        )


@router.put("/{customer_id}", response_model=BaseResponse[CustomerResponse])
async def update_customer(
    customer_id: UUID4,
    customer_data: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = CustomerService(db)
        updated_customer = await service.update_customer(customer_id, customer_data, user)
        
        if not updated_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return BaseResponse(
            status="Success",
            message="Customer updated successfully",
            data=CustomerResponse.model_validate(updated_customer)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error update customer: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error update customer: {e}",
                data=None
            ).model_dump()
        )


@router.delete("/{customer_id}", response_model=BaseResponse[dict])
async def delete_customer(
    customer_id: UUID4,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = CustomerService(db)
        deleted = await service.delete_customer(customer_id, user)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return BaseResponse(
            status="Success",
            message="Customer deleted successfully",
            data={"deleted": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error delete customer: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error delete customer: {e}",
                data=None
            ).model_dump()
        )