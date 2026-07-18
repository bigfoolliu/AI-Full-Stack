"""
安全
"""

from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET
from app.core.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验明文密码与 bcrypt 哈希是否匹配。"""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def validate_password_strength(password: str) -> str | None:
    """校验密码强度，返回 None 表示合规，否则返回中文提示。"""
    if len(password) < 8:
        return "密码长度不能少于 8 位"
    if not any(c.isupper() for c in password):
        return "密码必须包含至少一个大写字母"
    if not any(c.islower() for c in password):
        return "密码必须包含至少一个小写字母"
    if not any(c.isdigit() for c in password):
        return "密码必须包含至少一个数字"
    return None


def get_password_hash(password: str) -> str:
    """使用 bcrypt 对密码进行哈希。"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(data: dict) -> str:
    """生成包含用户 ID 和过期时间的 JWT token。"""
    to_encode = {}
    for k, v in data.items():
        to_encode[k] = str(v) if k == "sub" else v
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_db():
    """FastAPI 依赖注入：每个请求使用独立数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """解析 JWT token 返回当前用户，无效 token 返回 401。"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (JWTError, TypeError, ValueError):
        raise credentials_exception

    from app.models import User

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
