from pydantic import BaseModel


class LoginRequest(BaseModel):
    """登录请求体。"""

    username: str
    password: str


class UserInfo(BaseModel):
    """用户公开信息。"""

    id: int
    username: str
    nickname: str


class LoginResponseData(BaseModel):
    """登录成功的返回数据。"""

    token: str
    user: UserInfo
