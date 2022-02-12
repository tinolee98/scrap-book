from datetime import datetime
import jwt
from sqlalchemy.orm import Session

class AuthService:
    @staticmethod
    def verify_access_token(id: int, accessToken: str, expiredTime: datetime):
        jwt.encode

    @staticmethod
    def check_access_token(db: Session, accessToken: str, refreshToken: str, expiredTime: datetime):

        return id