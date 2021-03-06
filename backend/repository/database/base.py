from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase:
    """Базовый класс декларативного описания ORM моделей SQLAlchemy."""

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return cls.__name__.replace("DBModel", "").lower()  # type: ignore

    __mapper_args__ = {"eager_defaults": True}


Base = declarative_base(cls=CustomBase)
