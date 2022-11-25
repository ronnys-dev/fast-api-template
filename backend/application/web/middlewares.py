from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic.error_wrappers import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from application.web.exceptions import ErrorResponse, ValidationErrorResponse
from domain.base import DomainException


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
        except ValidationError as e:
            logger.exception(e)
            content = ValidationErrorResponse(
                status=status.HTTP_422_UNPROCESSABLE_ENTITY, error_message=e.errors()
            ).dict()
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=content,
            )
        except DomainException as e:
            logger.exception(e)
            content = ErrorResponse(status=e.status, error_message=e.message).dict()
            response = JSONResponse(status_code=e.status, content=content)

        return response


def init_middleware(app: FastAPI) -> None:
    """Initialize all middlewares in application."""
    app.add_middleware(ExceptionMiddleware)
