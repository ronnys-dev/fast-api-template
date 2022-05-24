from typing import List

from domain.product.exceptions import ProductDoesNotExist
from domain.product.repos import IProductRepo, Product
from sqlalchemy import Column, Float, Integer, String, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..database.base import Base
from ..database.database import DatabaseResource


class ProductDBModel(Base):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    weight = Column(Float)
    comment = Column(String)

    @classmethod
    def from_model(cls, product: Product) -> "ProductDBModel":
        return cls(
            name=product.name,
            price=product.price,
            weight=product.weight,
            comment=product.comment,
            id=product.id,
        )


class ProductDBRepo(IProductRepo):
    def __init__(self, db_resource: DatabaseResource):
        self._session = db_resource.session

    async def create(self, product: Product) -> Product:
        session: AsyncSession
        async with self._session() as session:
            db_product = ProductDBModel.from_model(product)
            session.add(db_product)
            await session.commit()
            await session.refresh(db_product)

        return Product.from_orm(db_product)

    async def list(self) -> List[Product]:
        session: AsyncSession
        async with self._session() as session:
            result = await session.execute(select(ProductDBModel))  # type: ignore
            products = [Product.from_orm(product) for product in result.scalars().all()]
        return products

    async def get(self, product_id: int) -> Product:
        session: AsyncSession
        async with self._session() as session:
            product = await session.get(ProductDBModel, product_id)
        if product is None:
            raise ProductDoesNotExist()
        return Product.from_orm(product)

    async def update(self, product_id: int, product: Product) -> Product:
        session: AsyncSession
        async with self._session() as session:
            db_product = await session.get(ProductDBModel, product_id)
            if db_product is None:
                raise ProductDoesNotExist()
            product_data = product.dict(exclude_unset=True)
            for field, value in product_data.items():
                setattr(db_product, field, value)
            session.add(db_product)
            await session.commit()
            await session.refresh(db_product)

        return Product.from_orm(db_product)

    async def delete(self, product_id: int) -> None:
        session: AsyncSession
        async with self._session() as session:
            product = await session.get(ProductDBModel, product_id)
            if product is None:
                raise ProductDoesNotExist()
            await session.delete(product)
            await session.commit()
