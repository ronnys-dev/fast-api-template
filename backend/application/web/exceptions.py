from typing import Any, Optional, Protocol, Type

from domain.base import DomainException
from pydantic import BaseModel


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[list[ErrorMessage]]


error_responses = {
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    403: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}


class _HttpException(Protocol):
    msg: str
    status: int
    domain_exception: Type[DomainException]


class HttpExceptionMeta(type):
    """Метакласс для маппинга доменных исключений к HTTP ответам."""

    registered_exceptions: dict[Type[DomainException], Type[_HttpException]] = {}

    def __new__(mcs, name: str, bases: tuple[type, ...], dct: dict[str, Any]) -> type:
        """Сохраняем сценарий в список."""
        mcs._validate_dct(name, dct)
        http_exception_class = super().__new__(mcs, name, bases, dct)
        mcs.registered_exceptions[
            dct["domain_exception"]
        ] = http_exception_class  # type: ignore[assignment]
        return http_exception_class

    @staticmethod
    def _validate_dct(name: str, dct: dict[str, Any]) -> None:
        required_fields = {
            "msg": str,
            "status": int,
            "domain_exception": DomainException,
        }
        for field, field_class in required_fields.items():
            if field_class in {int, str}:
                if not isinstance(dct[field], field_class):
                    raise ValueError(
                        "{}: '{}' is not an instance of '{}'".format(
                            name, dct[field], field_class
                        )
                    )
            elif field_class is DomainException:
                if not issubclass(dct[field], field_class):
                    raise ValueError(
                        "{}: '{}' is not a subclass of '{}'".format(
                            name, dct[field], field_class
                        )
                    )
            else:
                raise ValueError
