from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any


class PaginatedData(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
