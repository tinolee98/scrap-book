import uuid

from sqlalchemy.orm import Session

from src.sql.models import Scrapbook, User

class ScrapbookService:
    @staticmethod
    def get_scrapbooks(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first().scrapbooks

    @staticmethod
    def get_scrapbook_by_id(db: Session, id: int):
        return db.query(Scrapbook).filter(Scrapbook.id == id).first()

    @staticmethod
    def has_scrapbook(db: Session,  user_id: int, book_id: int):
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