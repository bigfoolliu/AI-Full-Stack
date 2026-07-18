from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel):
    """统一 API 响应格式。"""

    code: int
    message: str
    data: Any


class PaginatedData(BaseModel, Generic[T]):
    """分页数据包装。"""

    items: list[T]
    total: int
    page: int
    page_size: int
