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
