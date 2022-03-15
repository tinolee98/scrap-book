from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from src.sql.models import Book
from src.routes.apis.v1.book.schemas import BookIn

class BookService:
    @staticmethod
    def existed_book(db: Session, authors: str, title: str):
        return db.query(Book).filter(Book.authors == authors).filter(Book.title == title).first()
    
    @staticmethod
    def create_book(db:Session, book: BookIn):
        try:
            db_book = Book(title=book.title,
                authors=book.authors,
                publisher=book.publisher,
                contents=book.contents,
                thumbnail=book.thumbnail,
                url=book.url)
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            return db_book
        except:
            return None