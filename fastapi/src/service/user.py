from datetime import datetime
from sqlalchemy.orm import Session

from ..sql.models import User

from .auth import AuthService

class UserService:
    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, id: int):
        return db.query(User).filter(User.id == id)

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email)
        