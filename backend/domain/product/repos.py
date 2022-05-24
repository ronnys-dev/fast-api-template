from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    weight: float
    comment: Optional[str] = None

    class Config:
        orm_mode = True


class IProductRepo(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        """Создание продукта"""

    @abstractmethod
    async def list(self) -> List[Product]:
        """Вывод списка всех продуктов"""

    @abstractmethod
    async def get(self, product_id: int) -> Product:
        """Получение продукта по его id"""

    @abstractmethod
    async def update(self, product_id: int, product: Product) -> Product:
        """Обновление продукта"""

    @abstractmethod
    async def delete(self, product_id: int) -> None:
        """Удаление продукта"""
