from typing import Optional
import jwt

from fastapi import APIRouter, Body, Depends, status, Header, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.common.schema import OkError
from src.common.response import check_token
from src.config import Config
from src.common.response import verify_token
from src.service.user import UserService
from src.sql.database import get_db
from src.sql.models import User
from src.routes.apis.v1.auth.schemas import UserIn, LoginResult, UserOut

rt = APIRouter(
    prefix='/apis/v1/auth',
    tags=['apis/v1/auth']
)

@rt.post("/signUp", description="회원가입 API", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def sign_up(db: Session = Depends(get_db), user: UserIn = Body(...)):
    existed = UserService.get_user_by_email(db, user.email)
    if existed:
        return JSONResponse(content={
            "error": "already existed",
            "ok": False
            }, status_code=status.HTTP_200_OK)

    user_db = UserService.create_user(db, user)
    if not user_db:
        return JSONResponse(content={"error": "fail to create user", "ok": False}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    json_user_db = jsonable_encoder(user_db)
    return JSONResponse(content= json_user_db)

@rt.post('/login', description="로그인 API", response_model=LoginResult)
def log_in(db:Session = Depends(get_db), user: UserIn = Body(...)):
    user_db = UserService.get_user_by_email(db, user.email)
    if not user_db:
        return JSONResponse(content={
            "error": "user not existed",
            "ok": False
        })
    if not UserService.check_password(user.password, user_db.password):
        return JSONResponse(content={
            "error": "incorrect password",
            "ok": False
        })
    refreshToken = UserService.create_refresh_token(db, user_db.id)
    if not refreshToken:
        return {"error": "no refresh token", "ok": False}
    token = UserService.create_access_token(db, refreshToken)
    return JSONResponse(content={"ok": True, "accessToken":token["accessToken"], "exp": token["exp"], "refreshToken": refreshToken})

@rt.delete('/logOut', description="로그아웃 API", response_model=OkError)
def log_out(refreshToken: str = Header(...), db: Session = Depends(get_db)):
    if not UserService.delete_refresh_token(db, refreshToken):
        return JSONResponse(content={"ok": False, "error": "fail to log out"})
    return JSONResponse(content={"ok": True})

@rt.get('/{id}', description="ID 기반 유저 검색 API", response_model=UserOut)
def search(db:Session = Depends(get_db), id: int = 1):
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        return JSONResponse(content={"id": id, "email": db_user.email}) 
    return {"ok": False, "error": "fail to find an user"}

# @rt.post('/test/{id}', response_model=Token)
@rt.delete('/delete')
def delete(db:Session = Depends(get_db), user: User = Depends(verify_token)):
    return UserService.delete_user(db, user.id)

# response model 추가히기
@rt.post('/refresh', description="리프레시 API", response_model=LoginResult)
async def refresh(db: Session = Depends(get_db), refreshToken: Optional[str] = Depends(check_token)):
    if not refreshToken:
        return JSONResponse(content={"error": "invalid token", "ok": False}, status_code=status.HTTP_401_UNAUTHORIZED)
    token = UserService.create_access_token(db, refreshToken)
    refreshToken = UserService.create_refresh_token(db, token=token['accessToken'])
    if not refreshToken:
        return JSONResponse(content={"ok": False, "error": "invalid refreshToken"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return JSONResponse(content={"ok": True, "accessToken": token["accessToken"], "exp": token["exp"], "refreshToken": refreshToken})