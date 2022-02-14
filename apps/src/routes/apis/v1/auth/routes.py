import datetime
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.service.auth import AuthService
from src.sql.database import get_db
from src.sql.models import User
from .schemas import UserIn, Token

rt = APIRouter(prefix='/auth')

@rt.post("/signUp", description="회원가입 API", status_code=status.HTTP_201_CREATED)
def sign_up(db: Session = Depends(get_db), user: UserIn = Body(..., embed=True)):
    user_existed = db.query(User).filter(User.email == user.email).first()
    if user_existed:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "already existed"})
    db_user = User(email=user.email, password=user.password)
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  
    json_compatible_user = jsonable_encoder(db_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_compatible_user)

@rt.get('/{id}')
def search(db:Session = Depends(get_db), id: int = 1):
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        return db_user
    return {"message" : "fail to find"}

@rt.get('/test/{id}', response_model=Token)
def test(id:int = 1):
    token = AuthService.create_refresh_token(id)
    import time
    time.sleep(1)
    user_id = AuthService.verify_access_token(token)
    return token