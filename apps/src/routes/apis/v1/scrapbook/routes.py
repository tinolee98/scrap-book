from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.service.book import BookService
from src.service.scrapbooks import ScrapbookService
from src.sql.models import User
from src.sql.database import get_db
from src.common.response import verify_token
from src.routes.apis.v1.book.schemas import BookIn

rt = APIRouter(prefix='/apis/v1/scrapbook', tags=['/apis/v1/scrapbook'])

@rt.get('s/')
def get_scrapbooks(db: Session = Depends(get_db), user: User = Depends(verify_token)):
    scrapbooks = ScrapbookService.get_scrapbooks(db, user.id)
    res = JSONResponse(content={"scrapbooks": scrapbooks})
    return res

@rt.post('/', status_code=status.HTTP_201_CREATED)
def create_scrapbook(book: BookIn = Body(...), db: Session = Depends(get_db), user: User = Depends(verify_token)):
    db_book = BookService.existed_book(db, book.authors, book.title)
    if not db_book:
        db_book = BookService.create_book(db, book)
    if ScrapbookService.has_scrapbook(db, user.id, db_book.id):
        return JSONResponse(content={"error": "already scrapbook existed", "ok": False}, status_code=status.HTTP_200_OK)
    ok = ScrapbookService.create_scrapbook(db, user, db_book.id)
    if ok:
        return True
    return False
