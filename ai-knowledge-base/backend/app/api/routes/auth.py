from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_current_user,
    get_db,
    verify_password,
)
from app.models import User
from app.schemas.auth import LoginRequest, LoginResponseData, UserInfo
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/login", response_model=ApiResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> ApiResponse:
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    token = create_access_token(data={"sub": user.id})

    return ApiResponse(
        code=0,
        message="ok",
        data=LoginResponseData(
            token=token,
            user=UserInfo(id=user.id, username=user.username, nickname=user.nickname),
        ),
    )


@router.get("/me", response_model=ApiResponse)
def me(current_user: User = Depends(get_current_user)) -> ApiResponse:
    return ApiResponse(
        code=0,
        message="ok",
        data=UserInfo(
            id=current_user.id,
            username=current_user.username,
            nickname=current_user.nickname,
        ),
    )
