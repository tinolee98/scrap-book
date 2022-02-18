from typing import Optional
import bcrypt
import jwt
from jwt import DecodeError
import datetime

from sqlalchemy.orm import Session

from src.routes.apis.v1.auth.schemas import UserIn
from src.sql.models import User
from src.routes.apis.v1.auth.schemas import Token


from ..config import Config

class AuthService:
    @staticmethod
    def create_access_token(refreshToken: str):
        token_id = jwt.decode(refreshToken, Config.REFRESH_TOKEN_KEY, algorithms=Config.JWT_ALGORITHM)
        token = jwt.encode(token_id,Config.ACCESS_TOKEN_KEY, algorithm=Config.JWT_ALGORITHM)
        exp = str(round( (datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp()))
        return {
            "accessToken": token,
            "exp": exp
        }

    @staticmethod
    def create_refresh_token(db: Session, id: int):
        token = jwt.encode({"id": id}, Config.REFRESH_TOKEN_KEY, algorithm=Config.JWT_ALGORITHM)
        db.query(User).filter(User.id == id).update({User.refreshToken: token})
        db.commit()
        return token
    
    @staticmethod
    def create_user(db:Session, user: UserIn):
        try:    
            hashedPW = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            print(hashedPW)
            db_user = User(email=user.email, password=hashedPW)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return user
        except:
            return False

