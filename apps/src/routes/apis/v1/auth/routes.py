from typing import Optional
import jwt

from fastapi import APIRouter, Body, Depends, status, Header
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
from src.routes.apis.v1.auth.schemas import UserIn, UserToken, UserOut

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

@rt.post('/login', description="로그인 API", response_model=UserToken)
def log_in(db:Session = Depends(get_db), user: UserIn = Body(...)):
    user_db = UserService.get_user_by_email(db, user.email)
    if not user_db:
        return JSONResponse(content={
            "error": "user not existed",
            "ok": False
        })
    token = UserService.create_refresh_token(db, user_db.id)
    if not token:
        return {"error": "no token", "ok": False}
    token = UserService.create_access_token(db, token)
    response = JSONResponse(content={"id": user_db.id, "email": user_db.email, "accessToken":token["accessToken"], "exp": token["exp"]})
    response.set_cookie('token', token, httponly=True, secure=True)
    return response

@rt.get('/logOut', description="로그아웃 API", response_model=OkError)
def log_out():
    response = JSONResponse(content={"ok": True})
    response.set_cookie('token', '', httponly=True, secure=True)
    return response

@rt.get('/{id}')
def search(db:Session = Depends(get_db), id: int = 1):
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        return db_user
    return {"error": "fail to find an user"}

# @rt.post('/test/{id}', response_model=Token)
@rt.delete('/delete')
def delete(db:Session = Depends(get_db), user: User = Depends(verify_token)):
    return UserService.delete_user(db, user.id)

@rt.get('/refresh')
async def refresh(db: Session = Depends(get_db), refreshToken: Optional[str] = Depends(check_token)):
    if not refreshToken:
        return JSONResponse(content={"error": "invalid token", "ok": False}, status_code=status.HTTP_401_UNAUTHORIZED)
    headers = UserService.create_access_token(db, refreshToken)
    response = JSONResponse(content={"ok": True}, headers=headers)
    return response