from typing import List

from domain.base import UseCaseMeta
from domain.product.repos import IProductRepo, Product


class CreateProductUseCase(metaclass=UseCaseMeta):
    def __init__(self, repo: IProductRepo):
        self._repo = repo

    async def execute(self, product: Product) -> Product:
        return await self._repo.create(product)


class GetProductUseCase(metaclass=UseCaseMeta):
    def __init__(self, repo: IProductRepo):
        self._repo = repo

    async def execute(self, product_id: int) -> Product:
        product = await self._repo.get(product_id)
        return product


class ListProductUseCase(metaclass=UseCaseMeta):
    def __init__(self, repo: IProductRepo):
        self._repo = repo

    async def execute(self) -> List[Product]:
        return await self._repo.list()


class UpdateProductUseCase(metaclass=UseCaseMeta):
    def __init__(self, repo: IProductRepo):
        self._repo = repo

    async def execute(self, product_id: int, product: Product):
        return await self._repo.update(product_id, product)


class DeleteProductUseCase(metaclass=UseCaseMeta):
    def __init__(self, repo: IProductRepo):
        self._repo = repo

    async def execute(self, product_id: int) -> None:
        await self._repo.delete(product_id)
