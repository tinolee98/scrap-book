import bcrypt
import jwt
from jwt import DecodeError
import datetime
import json
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from src.routes.apis.v1.auth.schemas import UserIn
from src.sql.models import User

from src.routes.apis.v1.auth.schemas import Token


from ..config import Config

class AuthService:
    @staticmethod
    def create_access_token(id: int):
        token = jwt.encode({"id":id},Config.ACCESS_TOKEN_KEY, algorithm=Config.JWT_ALGORITHM)
        exp = str(round( (datetime.datetime.now() + datetime.timedelta(minutes=30)).timestamp()))
        # exp = datetime.datetime.now()
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
    def verify_access_token(token: Token):
        try:
            # wrong token
            # result = jwt.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjB9.SeBaGVWU4IhClHziwk8d2Pz1a9z7XlIKsjlNGsvljgy", Config.ACCESS_TOKEN_KEY,algorithms=Config.JWT_ALGORITHM) 
            id = jwt.decode(token["accessToken"], Config.ACCESS_TOKEN_KEY,algorithms=Config.JWT_ALGORITHM)
            if token["exp"] < datetime.datetime.now():
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Expired Token")
            return id
        except jwt.DecodeError as e:
            print(e, "wrong token")
            return False

    @staticmethod
    def verify_refresh_token(db: Session, token: Token):
        try:
            id = jwt.decode(token["accessToken"], Config.ACCESS_TOKEN_KEY,algorithms=Config.JWT_ALGORITHM)
            user = db.query(User).filter(User.id == id).first()
            print(token["refreshToken"])
            if token["refreshToken"] == user.refreshToken:
                print("ok")
        except:
            return False
        return id
    
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

