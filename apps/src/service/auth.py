import jwt
import datetime
import json
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.sql.models import User

from src.routes.apis.v1.auth.schemas import Token


from ..config import Config

class AuthService:
    @staticmethod
    def create_access_token(id: int):
        token = jwt.encode({"id":id},Config.ACCESS_TOKEN_KEY, algorithm=Config.JWT_ALGORITHM)
        exp = datetime.datetime.now() + datetime.timedelta(minutes=30)
        # exp = datetime.datetime.now()
        return {
            "accessToken": token,
            "exp": exp
        }

    @staticmethod
    def create_refresh_token(db: Session, id: int):
        token = jwt.encode({"id": id}, Config.REFRESH_TOKEN_KEY, algorithm=Config.JWT_ALGORITHM)
        db.query(User).filter(User.id == id).update({User.refreshToken: token})
        accessAndExp = AuthService.create_access_token(id)
        return {
                **accessAndExp,
                "refreshToken": token,
        }

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
            userRefreshToken = db.query(User).filter(User)
        except:
            return False
        return id