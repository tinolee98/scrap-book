import datetime
import jwt


from typing import Optional

from fastapi import Depends, HTTPException, Header, status, Request
from sqlalchemy.orm import Session
from apps.src.service.user import UserService
from src.sql.models import User
from src.sql.database import get_db

from src.config import Config


async def verify_token(
    token:Optional[str] = Header(None),
    exp: Optional[str] = Header(None),
    db: Session = Depends(get_db)
    ):
    if not token or not exp:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "invalid_token", "ok": False})
    try:
        token_id = jwt.decode(token, Config.ACCESS_TOKEN_KEY, algorithms=Config.JWT_ALGORITHM)
        id = token_id["id"]
        if not token_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "invalid_token", "ok": False})
    except jwt.DecodeError as e:
        print(e)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "invalid_token", "ok": False})
    now = round(datetime.now().timestamp())
    # 만료된 토큰인 경우 refresh token를 이용해 access token 모두 새로 발급 필요
    if int(exp)-now < 30:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "expired_token", "ok": False})

    current_user = UserService.get_user_by_id(db, id)
    if not current_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail={"error": "Not existed user", "ok": False})
    return current_user

