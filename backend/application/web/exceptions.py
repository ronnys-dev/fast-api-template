from typing import Any, Optional, Protocol, Type, List, Dict

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: int
    error_message: str


class ValidationErrorResponse(BaseModel):
    status: int
    error_message: List[Dict]


error_responses = {
    400: {"model": ErrorResponse},
    401: {"model": ErrorResponse},
    403: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    422: {"model": ValidationErrorResponse},
    500: {"model": ErrorResponse},
}