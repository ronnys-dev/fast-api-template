from application.web.exceptions import HttpExceptionMeta
from domain.product.exceptions import ProductDoesNotExist
from fastapi import status


class ProductDoesNotExistHttpError(metaclass=HttpExceptionMeta):
    """Продукт не найден."""

    msg = "Product does not exist."
    status = status.HTTP_404_NOT_FOUND

    domain_exception = ProductDoesNotExist
