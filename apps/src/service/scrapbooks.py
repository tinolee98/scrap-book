from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from src.sql.models import Scrapbook, User, ScrapbookStar, Scrap, Book

class ScrapbookService:
    @staticmethod
    def get_scrapbooks(db: Session, user_id: int, limit: int, offset: int):
        result = []
        scrapbooks = db.query(User).filter(User.id == user_id).first().scrapbooks.offset(offset).limit(limit).all()
        for scrapbook in scrapbooks:
            scrapbook.star = ScrapbookService.is_starred(db, scrapbook.id, user_id)
            scrapbook.book
            scrapbook.countScraps = ScrapbookService.count_scraps(db, scrapbook.id)
            result.append(scrapbook)
        return result

    @staticmethod
    def get_scrapbook_by_id(db: Session, scrapbook_id: int, user_id: int):
        scrapbook = db.query(Scrapbook).filter(Scrapbook.id == scrapbook_id).first()
        if not scrapbook:
            return None
        scrapbook.star = ScrapbookService.is_starred(db, scrapbook.id, user_id)
        scrapbook.countScraps = ScrapbookService.count_scraps(db, scrapbook.id)
        return scrapbook

    @staticmethod
    def is_starred(db: Session, scrapbook_id: int, user_id: int):
        star = db.query(ScrapbookStar) \
            .filter(ScrapbookStar.scrapbookId == scrapbook_id) \
            .filter(ScrapbookStar.userId == user_id) \
            .first()
        return star.is_starred
    
    @staticmethod
    def on_star(db: Session, scrapbook_id: int, user_id: int):
        try:
            db.query(ScrapbookStar).filter(ScrapbookStar.scrapbookId == scrapbook_id).filter(ScrapbookStar.userId == user_id).update({ScrapbookStar.is_starred: True})
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def off_star(db: Session, scrapbook_id: int, user_id: int):
        try:
            db.query(ScrapbookStar).filter(ScrapbookStar.scrapbookId == scrapbook_id).filter(ScrapbookStar.userId == user_id).update({ScrapbookStar.is_starred: False})
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def count_scraps(db: Session, scrapbook_id: int):
        return db.query(Scrap).filter(Scrap.scrapbookId == scrapbook_id).count()


    @staticmethod
    def create_star(db: Session, scrapbook_id: int, user_id: int):
        try:
            newScrapbookStar = ScrapbookStar(userId=user_id, scrapbookId=scrapbook_id)
            db.add(newScrapbookStar)
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def delete_star(db: Session, scrapbook_id: int, user_id: int):
        try:
            db_scrapbook_star = db.query(ScrapbookStar) \
                                    .filter(ScrapbookStar.userId == user_id) \
                                    .filter(ScrapbookStar.scrapbookId == scrapbook_id) \
                                    .first()
            db.delete(db_scrapbook_star)
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def scrapbook_already_exists(user: User, book_id: int):
        scrapbooks = user.scrapbooks.all()
        for scrapbook in scrapbooks:
            if scrapbook.bookId == book_id:
                return True
        return False

    @staticmethod
    def create_scrapbook(db: Session, user: User, book_id: int):
        try:
            book_uuid = str(uuid.uuid4())
            db_scrapbook = Scrapbook(uuid=book_uuid, bookId=book_id)
            user.scrapbooks.append(db_scrapbook)
            db.add(db_scrapbook)
            db.add(user)
            db.commit()
            return db_scrapbook
        except:
            return False

    @staticmethod
    def join_scrapbook(db: Session, user_id: int, scrapbook: Scrapbook):
        try:
            star = ScrapbookStar(userId=user_id, scrapbookId=scrapbook.id)
            scrapbook.stars.append(star)
            db.add(star)
            db.add(scrapbook)
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def go_out_scrapbook(db: Session, user: User, scrapbook: Scrapbook):
        scrapbook.users.remove(user)
        if len(scrapbook.users) == 0:
            if ScrapbookService.delete_scrapbook(db, scrapbook):
                return True
            else:
                return False
        db.commit()
        db.refresh(scrapbook)
        return True

    @staticmethod
    def delete_scrapbook(db: Session, scrapbook: Scrapbook):
        try:
            db.delete(scrapbook)
            db.commit()
            return True
        except:
            return False