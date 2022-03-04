from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from src.common.schema import OkError

class UserBase(BaseModel):
    email: EmailStr = Field(..., title="유저 이메일", example="mingo@scrap.com")

class UserIn(UserBase):
    password: str = Field(..., title="비밀번호", example="1234")

class UserOut(UserBase):
    id: int = Field(..., title="유저 아이디", example="1")

class UserInDB(UserBase):
    password: str = Field(...,
        title="암호화 비밀번호", 
        example="hashed password",
        description="DB에 저장되는 암호화된 패스워드"
    )
    class Config:
        orm_mode = True

class LoginResult(OkError):
    accessToken: Optional[str] = Field(None, title="액세스 토큰", example="1234567accessToken")
    exp: Optional[str] = Field(None, title="만료 시간", example="1234567expiredTime")
    refreshToken: Optional[str] = Field(None, title="리프레시 토큰", example="1234567refreshToken")
    class Config:
        orm_mode = True