from ast import Str
from typing import Text
from sqlalchemy.orm import Session

from src.sql.models import Scrap, Scrapbook

class ScrapService:
    @staticmethod
    def create_scrap(db: Session, user_id: int, scrapbook_id: int, text: Text, page: int, picture_url: Str):
        try:
            new_scrap = Scrap(userId=user_id, scrapbookId=scrapbook_id, text=text, page=page, picture=picture_url)
            db.add(new_scrap)
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def update_scrap(db: Session, scrap: Scrap):
        try:
            db.commit()
            db.refresh(scrap)
            return True
        except:
            return False

    @staticmethod
    def delete_scrap(db: Session, scrap_id: int):
        try:
            db.query(Scrap).filter(Scrap.id == scrap_id).delete()
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def get_scrap_by_id(db: Session, scrap_id: int):
        return db.query(Scrap).filter(Scrap.id == scrap_id).first()
