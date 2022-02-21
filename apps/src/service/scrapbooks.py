from sqlalchemy.orm import Session

from src.sql.models import Scrapbook, User

class ScrapbookService:
    @staticmethod
    def get_scrapbooks(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first().scrapbooks

    @staticmethod
    def get_scrapbook_by_id(db: Session, id: int):
        return db.query(Scrapbook).filter(Scrapbook.id == id).first()