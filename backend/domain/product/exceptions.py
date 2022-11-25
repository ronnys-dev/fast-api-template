from domain.base import DomainException
from fastapi import status


class ProductDoesNotExist(DomainException):
    """Продукт не найден"""

    status = status.HTTP_404_NOT_FOUND
    message = 'Product does not exist'
