from application.web.exceptions import error_responses
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from .product.api import router as product_router

api_router = APIRouter(
    default_response_class=JSONResponse,
    responses=error_responses,  # type: ignore
)


# api routers
api_router.include_router(product_router, prefix="/products", tags=["product"])


@api_router.get("/health_check", include_in_schema=False)
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


def init_routers(app: FastAPI) -> None:
    """Initialize all routers in application."""
    app.include_router(api_router, prefix="/api")
