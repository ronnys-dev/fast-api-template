from functools import lru_cache

import punq  # type: ignore
from common.config import AppConfig, DatabaseConfig
from domain.base import UseCaseMeta
from domain.product.repos import IProductRepo
from repository.database.database import DatabaseResource
from repository.product.product_db_repo import ProductDBRepo


@lru_cache(maxsize=1)
def get_container() -> punq.Container:
    """Singleton фабрика DI контейнера."""
    return _initialize_container()


def _initialize_container() -> punq.Container:
    """Инициализация DI контейнера."""
    container = punq.Container()

    # Config
    container.register(AppConfig, instance=AppConfig())
    container.register(DatabaseConfig, instance=DatabaseConfig())

    # Resources
    container.register(DatabaseResource, factory=DatabaseResource)

    # Repos
    container.register(IProductRepo, factory=ProductDBRepo)  # type: ignore[misc]

    # Use Cases
    for use_case in UseCaseMeta.registered_use_cases:
        container.register(use_case)

    return container
