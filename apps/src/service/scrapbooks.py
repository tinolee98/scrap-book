import uuid

from sqlalchemy.orm import Session

from src.sql.models import Scrapbook, User, ScrapbookStar

class ScrapbookService:
    @staticmethod
    def get_scrapbooks(db: Session, user_id: int):
        result = []
        scrapbooks = db.query(User).filter(User.id == user_id).first().scrapbooks
        for scrapbook in scrapbooks:
            scrapbook.star = ScrapbookService.is_starred(db, scrapbook.id)
            result.append(scrapbook)
        return result

    @staticmethod
    def get_scrapbook_by_id(db: Session, scrapbook_id: int, user_id: int):
        scrapbook = db.query(Scrapbook).filter(Scrapbook.id == scrapbook_id).first()
        if not scrapbook:
            return None
        scrapbook.star = ScrapbookService.is_starred(db, scrapbook.id, user_id)
        return scrapbook

    @staticmethod
    def is_starred(db: Session, scrapbook_id: int, user_id: int):
        if db.query(ScrapbookStar) \
            .filter(ScrapbookStar.scrapbookId == scrapbook_id) \
            .filter(ScrapbookStar.userId == user_id) \
            .first():
            return True
        return False
    
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
    def scrapbook_already_exists(db: Session,  user_id: int, book_id: int):
        scrapbooks = ScrapbookService.get_scrapbooks(db, user_id)
        for scrapbook in scrapbooks:
            if scrapbook.bookId == book_id:
                return True
        return False

    @staticmethod
    def create_scrapbook(db: Session, user: User, book_id: int):
        try:
            book_uuid = str(uuid.uuid4())
            db_scrapbook = Scrapbook(uuid=book_uuid, bookId=book_id)
            print(user.scrapbooks)
            user.scrapbooks.append(db_scrapbook)
            print(user.scrapbooks)
            db.add(db_scrapbook)
            db.add(user)
            db.commit()
            return True
        except:
            return False

    @staticmethod
    def delete_scrapbook(db: Session, scrapbook: Scrapbook):
        db.delete(scrapbook)
        db.commit()