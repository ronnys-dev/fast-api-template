from domain.base import DomainException


class ProductDoesNotExist(DomainException):
    """Продукт не найден"""
