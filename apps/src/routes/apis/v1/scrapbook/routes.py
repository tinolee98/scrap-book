from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.common.response import error
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
        return {"ok": True}
    return {"ok": False}

@rt.get('/{scrapbook_id}/')
def get_scraps_in_scrapbook(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id)
    if not db_scrapbook:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error(40400, "스크랩북이 존재하지 않습니다."))
    for scrapbook_user in db_scrapbook.users:
        if user.id == scrapbook_user.id:
            res = JSONResponse(content=jsonable_encoder(db_scrapbook))
            return res

@rt.delete('/{scrapbook_id}/')
def delete_scrapbook(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id)
    if not db_scrapbook:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error(40400, "스크랩북이 존재하지 않습니다."))
    ScrapbookService.delete_scrapbook(db, db_scrapbook)
    return {"ok": True}