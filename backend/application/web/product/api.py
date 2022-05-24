from typing import List

from application.common.container import get_container
from application.web.product.schemas import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from domain.product import use_cases
from domain.product.repos import Product
from fastapi import APIRouter, Depends, status
from punq import Container  # type: ignore
from starlette.responses import Response

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def product_create(
    product: ProductCreate, container: Container = Depends(get_container)
) -> ProductResponse:
    product_dto = Product.from_orm(product)
    created_product = await container.resolve(use_cases.CreateProductUseCase).execute(
        product_dto
    )
    return ProductResponse.from_orm(created_product)


@router.get("/", response_model=List[ProductResponse])
async def products_list(container: Container = Depends(get_container)):
    products = await container.resolve(use_cases.ListProductUseCase).execute()
    products_response = [ProductResponse.from_orm(product) for product in products]
    return products_response


@router.get("/{product_id}", response_model=ProductResponse)
async def product_get(product_id: int, container: Container = Depends(get_container)):
    product = await container.resolve(use_cases.GetProductUseCase).execute(product_id)
    return ProductResponse.from_orm(product)


@router.patch("/{product_id}", response_model=ProductResponse)
async def product_update(
    product_id: int,
    product: ProductUpdate,
    container: Container = Depends(get_container),
):
    product_dto = Product.from_orm(product)
    updated_product = await container.resolve(use_cases.UpdateProductUseCase).execute(
        product_id, product_dto
    )
    return ProductResponse.from_orm(updated_product)


@router.delete("/{product_id}")
async def product_delete(
    product_id: int, container: Container = Depends(get_container)
):
    await container.resolve(use_cases.DeleteProductUseCase).execute(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
