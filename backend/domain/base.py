from typing import Any, Type


class DomainException(Exception):
    """Исключение доменной логики"""

    exceptions: list[Type["DomainException"]] = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.exceptions.append(cls)


class UseCaseMeta(type):
    """Мета-класс сценария.

    Им удобно собирать все сценарии и регистрировать их в DI контейнер.
    """

    registered_use_cases: list[type] = []

    def __new__(mcs, *args: list[Any], **kwargs: dict[str, Any]) -> type:
        """Сохраняем сценарий в список."""
        use_case_class = super().__new__(mcs, *args, **kwargs)
        UseCaseMeta.registered_use_cases.append(use_case_class)
        return use_case_class
