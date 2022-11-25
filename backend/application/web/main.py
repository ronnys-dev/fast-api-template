import uvicorn  # type: ignore
from application.web.exceptions import ValidationErrorResponse
from application.web.logging import init_logging
from application.web.middlewares import init_middleware
from common.config import AppConfig
from common.container import get_container
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette import status
from starlette.responses import JSONResponse

from .routers import init_routers

init_logging()

import tracemalloc

tracemalloc.start()

def init_app() -> FastAPI:
    """Create the Web API framework."""
    app = FastAPI(
        title="Fast Api Template",
        docs_url="/swagger",
        openapi_url="/docs/openapi.json",
        redoc_url="/docs",
    )
    init_middleware(app=app)
    init_routers(app=app)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.exception(exc)
        content = ValidationErrorResponse(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY, error_message=exc.errors()
        ).dict()
        response = JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)
        return response

    return app


app = init_app()

container = get_container()
app_config = container.resolve(AppConfig)


if __name__ == "__main__":
    uvicorn.run(
        "application.web.main:app",
        host=app_config.server_host,
        port=app_config.server_port,
        reload=True,
    )
