import uvicorn  # type: ignore
from application.common.container import get_container
from application.web.exceptions import HttpExceptionMeta
from application.web.logging import init_logging
from application.web.middlewares import init_middleware
from common.config import AppConfig
from domain.base import DomainException
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from .routers import init_routers

init_logging()


def init_app() -> FastAPI:
    """Create the Web API framework."""
    app = FastAPI(
        title="Fast Api microservice",
        docs_url="/swagger",
        openapi_url="/docs/openapi.json",
        redoc_url="/docs",
    )
    init_middleware(app=app)
    init_routers(app=app)

    @app.exception_handler(DomainException)
    async def domain_exception_handler(
        _: Request, exc: DomainException
    ) -> JSONResponse:
        http_exception = HttpExceptionMeta.registered_exceptions[exc.__class__]
        return JSONResponse(
            {
                "detail": [{"msg": http_exception.msg}],
            },
            status_code=http_exception.status,
        )

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
