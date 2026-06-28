from fastapi import APIRouter

from app.core.config import MOCK_PASSWORD, MOCK_TOKEN, MOCK_USERNAME, MOCK_USER
from app.schemas.auth import LoginRequest, LoginResponseData, UserInfo
from app.schemas.common import ApiResponse

# 后面的接口格式，统一为 /api/xx
router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=ApiResponse)
def login(payload: LoginRequest) -> ApiResponse:
    print(payload, type(payload))
    if payload.username != MOCK_USERNAME or payload.password != MOCK_PASSWORD:
        return ApiResponse(code=1, message="用户名或密码错误", data=None)

    return ApiResponse(
        code=0,
        message="ok",
        data=LoginResponseData(
            token=MOCK_TOKEN,
            user=UserInfo(**MOCK_USER),
        ),
    )


@router.get("/me", response_model=ApiResponse)
def me() -> ApiResponse:
    return ApiResponse(
        code=0,
        message="ok",
        data=UserInfo(**MOCK_USER),
    )
