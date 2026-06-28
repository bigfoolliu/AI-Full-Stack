from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: int
    username: str
    nickname: str


class LoginResponseData(BaseModel):
    token: str
    user: UserInfo
