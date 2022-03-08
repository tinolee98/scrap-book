from ast import Str
from typing import Text
from sqlalchemy.orm import Session

from src.sql.models import Scrap, Scrapbook

class ScrapService:
    @staticmethod
    def create_scrap(db: Session, user_id: int, scrapbook_id: int, text: Text, page: int, picture_url: Str):
        try:
            new_scrap = Scrap(user_id=user_id, scrapbook_id=scrapbook_id, text=text, page=page, picture_url=picture_url)
            db.add(new_scrap)
            db.commit()
            return True
        except:
            return False