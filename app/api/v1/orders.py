from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdate, OrderWithItemsResponse
from app.schemas.sys_schema import BaseResponse, TokenData
from app.services.order_service import OrderService
from app.utils.sys import get_db, get_current_user


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/", response_model=BaseResponse[List[OrderWithItemsResponse]])
async def get_orders(
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of orders to return"),
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = OrderService(db)
        orders = await service.get_orders(user, skip, limit)
        
        return BaseResponse(
            status="Success",
            message="Berhasil mengambil data orders",
            data=[OrderWithItemsResponse.model_validate(order) for order in orders]
        )
        
    except Exception as e:
        print(f"Error get orders: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error get orders: {e}",
                data=None
            ).model_dump()
        )


@router.get("/{order_id}", response_model=BaseResponse[OrderWithItemsResponse])
async def get_order_by_id(
    order_id: UUID4,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = OrderService(db)
        order = await service.get_order_by_id(order_id, user)
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return BaseResponse(
            status="Success",
            message="Berhasil mengambil data order",
            data=OrderWithItemsResponse.model_validate(order)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error get order: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error get order: {e}",
                data=None
            ).model_dump()
        )


@router.post("/", response_model=BaseResponse[OrderWithItemsResponse])
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = OrderService(db)
        result = await service.create_order(order_data, user)
        
        return BaseResponse(
            status="Success",
            message="Order created successfully",
            data=OrderWithItemsResponse.model_validate(result)
        )
        
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content=BaseResponse(
                status="Error",
                message=f"Validation error: {ve}",
                data=None
            ).model_dump()
        )
    except Exception as e:
        print(f"Error create order: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error create order: {e}",
                data=None
            ).model_dump()
        )


@router.put("/{order_id}", response_model=BaseResponse[OrderWithItemsResponse])
async def update_order(
    order_id: UUID4,
    order_data: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = OrderService(db)
        updated_order = await service.update_order(order_id, order_data, user)
        
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return BaseResponse(
            status="Success",
            message="Order updated successfully",
            data=OrderWithItemsResponse.model_validate(updated_order)
        )
        
    except HTTPException:
        raise
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content=BaseResponse(
                status="Error",
                message=f"Validation error: {ve}",
                data=None
            ).model_dump()
        )
    except Exception as e:
        print(f"Error update order: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error update order: {e}",
                data=None
            ).model_dump()
        )


@router.delete("/{order_id}", response_model=BaseResponse[dict])
async def delete_order(
    order_id: UUID4,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = OrderService(db)
        deleted = await service.delete_order(order_id, user)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return BaseResponse(
            status="Success",
            message="Order deleted successfully",
            data={"deleted": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error delete order: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error delete order: {e}",
                data=None
            ).model_dump()
        )