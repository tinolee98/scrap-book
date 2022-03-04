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
    def get_user_by_token(db: Session, token: str):
        return db.query(User).filter(User.refreshToken == token).first()

    @staticmethod
    def delete_refresh_token(db: Session, id: int):
        pass

    @staticmethod
    def compare_token(db:Session, token: str, id: int):
        user = UserService.get_user_by_id(db, id)
        if user.refreshToken == token:
            return True
        return False

    @staticmethod
    def create_access_token(db: Session, refreshToken: str):
        user = UserService.get_user_by_token(db, refreshToken)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="invalid token")
        exp = str(round( (datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp()))
        iet = str(round(datetime.datetime.now().timestamp()))
        token = jwt.encode({"id": user.id, "exp": exp, "iet": iet}, Config.ACCESS_TOKEN_KEY, algorithm=Config.JWT_ALGORITHM)
        return {
            "accessToken": token,
            "exp": 30
        }

    @staticmethod
    def create_refresh_token(db: Session, id: int = None, token: str = None):
        iet = str(round(datetime.datetime.now().timestamp()))
        if token:
            try:
                token_id = jwt.decode(token, Config.ACCESS_TOKEN_KEY, algorithms=Config.JWT_ALGORITHM)
                id = token_id['id']
            except jwt.DecodeError as e:
                print(e)
                return False
            except jwt.ExpiredSignatureError as e:
                print(e)
                return False
        elif not id:
            return False
        refreshToken = jwt.encode({"id": id, "iet": iet}, Config.REFRESH_TOKEN_KEY, algorithm=Config.JWT_ALGORITHM)
        db.query(User).filter(User.id == id).update({User.refreshToken: refreshToken})
        db.commit()
        return refreshToken
    
    @staticmethod
    def check_password(password: str, password_db: str):
        password_db = password_db.encode('utf-8')
        password = password.encode('utf-8')
        return bcrypt.checkpw(password, password_db)

    @staticmethod
    def create_user(db:Session, user: UserIn):
        try:    
            hashedPW = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            hashedPW = hashedPW.decode('utf-8')
            db_user = User(email=user.email, password=hashedPW)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete_user(db: Session, id: id):
        user = UserService.get_user_by_id(db, id)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "user not existed"})
        db.query(User).filter(User.id == user.id).delete()
        db.commit()
        return {"ok": True}