from pydantic import BaseModel


class _ProductBase(BaseModel):
    name: str
    price: float
    weight: float
    comment: str | None = None


class ProductResponse(_ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductCreate(_ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    weight: float | None = None
    comment: str | None = None
