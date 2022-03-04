import requests
from time import time

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.service.book import BookService
from src.sql.models import Book, User
from src.sql.database import get_db
from src.service.user import UserService
from src.config import Config
from src.routes.apis.v1.book.schemas import BookIn

rt = APIRouter(prefix='/apis/v1/book', tags=['/apis/v1/book'])
URL = Config.KAKAO_BOOK_SEARCH_URL

@rt.get('s')
async def search_books(name: str):
    params = {"query": name}
    headers = {'Authorization': "KakaoAK {}".format(Config.KAKAO_BOOK_SEARCH_API_KEY)}
    book_res = requests.get(url=URL, params=params, headers=headers)
    return book_res.json()

@rt.post('')
async def create_book(book: BookIn = Body(...), db: Session = Depends(get_db)):
    if not book:
        return {"ok": False}
    existedBook = BookService.existed_book(db, book.authors, book.title)
    print(existedBook)
    ok = True
    if not existedBook:
        ok = BookService.create_book(db, book)
    return {"ok": ok}