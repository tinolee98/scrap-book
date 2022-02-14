from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr = Field(..., title="유저 이메일", example="user@example.com")

class UserIn(UserBase):
    password: str = Field(..., title="비밀번호", example="1234")

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    password: str = Field(...,
        title="암호화 비밀번호", 
        example="hashed password",
        description="DB에 저장되는 암호화된 패스워드"
    )
    class Config:
        orm_mode = True

class Token(BaseModel):
    accessToken: str = Field(..., title="액세스 토큰", example="access token")
    refreshToken: str = Field(..., title="리프레시 토큰", example="refresh token")
    exp: datetime = Field(..., title="만료 시간", example="1234-56-78T90:12:34.567890")
    class Config:
        orm_mode = True