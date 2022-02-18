import bcrypt
import jwt
import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.routes.apis.v1.auth.schemas import UserIn
from src.config import Config
from ..sql.models import User

class UserService:
    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, id: int):
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def compare_token(db:Session, token: str, id: int):
        user = UserService.get_user_by_id(db, id)
        if user.refreshToken == token:
            return True
        return False

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
            return db_user
        except:
            return False

    @staticmethod
    def delete_user(db: Session, id: id):
        user = UserService.get_user_by_id(db, id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "user not existed"})
        db.query(User).filter(User.id == user.id).delete()
        db.commit()
        return {"ok": True}