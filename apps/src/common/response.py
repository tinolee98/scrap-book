import datetime
import jwt

from typing import Optional

from fastapi import Depends, HTTPException, Header, status, Request
from sqlalchemy.orm import Session
from src.service.user import UserService
from src.sql.models import User
from src.sql.database import get_db

from src.config import Config

def error(code, error = None,ok=False):
    if not error:
        error = Config.ERROR_CODE[code]
    detail = {
        'error': error,
        'ok': ok
    }

    return detail

async def check_token(request: Request, db: Session = Depends(get_db), token: Optional[str] = Header(...), exp: Optional[str]= Header(...)):
    refreshToken = request.cookies.get('token')
    if not refreshToken or not token or not exp:
        return None
    user = UserService.get_user_by_token(db, refreshToken)
    if not user:
        return None
    try:
        token_id = jwt.decode(token, Config.ACCESS_TOKEN_KEY, Config.JWT_ALGORITHM)
        id = token_id['id']
    except jwt.DecodeError as e:
        print(e)
        return None
    if user.id == id:
        return refreshToken
    return None

async def verify_token(
    accesstoken:Optional[str] = Header(None),
    exp: Optional[str] = Header(None),
    db: Session = Depends(get_db)
    ):
    if not accesstoken or not exp:
        return None
    try:
        token_id = jwt.decode(accesstoken, Config.ACCESS_TOKEN_KEY, algorithms=Config.JWT_ALGORITHM)
        id = token_id["id"]
        if not token_id:
            return None
    except jwt.DecodeError as e:
        print(e)
        return None
    except jwt.ExpiredSignatureError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "expired token", "ok": False})
    now = round(datetime.datetime.now().timestamp())
    if int(exp)-now < 0:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "expired_token", "ok": False})

    current_user = UserService.get_user_by_id(db, id)
    return current_user

