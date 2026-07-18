"""
健康检查 api
"""

from fastapi import APIRouter

from app.schemas.common import ApiResponse

router = APIRouter()


@router.get("/health", response_model=ApiResponse)
def health() -> ApiResponse:
    """健康检查接口。"""
    return ApiResponse(code=0, message="ok", data={"status": "ok"})
