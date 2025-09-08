from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.schemas.sys_schema import BaseResponse, TokenData
from app.services.product_service import ProductService
from app.utils.sys import get_db, get_current_user


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=BaseResponse[List[ProductResponse]])
async def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of products to return"),
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        products = await service.get_products(user, skip, limit)
        
        return BaseResponse(
            status="Success",
            message="Berhasil mengambil data products",
            data=[ProductResponse.model_validate(product) for product in products]
        )
        
    except Exception as e:
        print(f"Error get products: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error get products: {e}",
                data=None
            ).model_dump()
        )


@router.get("/{product_id}", response_model=BaseResponse[ProductResponse])
async def get_product_by_id(
    product_id: UUID4,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        product = await service.get_product_by_id(product_id, user)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return BaseResponse(
            status="Success",
            message="Berhasil mengambil data product",
            data=ProductResponse.model_validate(product)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error get product: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error get product: {e}",
                data=None
            ).model_dump()
        )


@router.post("/", response_model=BaseResponse[ProductResponse])
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        result = await service.create_product(product_data, user)
        
        return BaseResponse(
            status="Success",
            message="Product created successfully",
            data=ProductResponse.model_validate(result)
        )
        
    except Exception as e:
        print(f"Error create product: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error create product: {e}",
                data=None
            ).model_dump()
        )


@router.put("/{product_id}", response_model=BaseResponse[ProductResponse])
async def update_product(
    product_id: UUID4,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        updated_product = await service.update_product(product_id, product_data, user)
        
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return BaseResponse(
            status="Success",
            message="Product updated successfully",
            data=ProductResponse.model_validate(updated_product)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error update product: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error update product: {e}",
                data=None
            ).model_dump()
        )


@router.delete("/{product_id}", response_model=BaseResponse[dict])
async def delete_product(
    product_id: UUID4,
    db: AsyncSession = Depends(get_db),
    user: TokenData = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        deleted = await service.delete_product(product_id, user)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return BaseResponse(
            status="Success",
            message="Product deleted successfully",
            data={"deleted": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error delete product: {e}")
        return JSONResponse(
            status_code=500,
            content=BaseResponse(
                status="Error",
                message=f"Error delete product: {e}",
                data=None
            ).model_dump()
        )