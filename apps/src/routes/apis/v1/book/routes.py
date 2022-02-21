import requests
from time import time

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import Field
from sqlalchemy.orm import Session

from src.sql.models import Book
from src.sql.database import get_db
from src.service.user import UserService
from src.config import Config
from src.routes.apis.v1.book.schemas import BookInfo

rt = APIRouter(prefix='/apis/v1/book', tags=['/apis/v1/book'])
URL = Config.KAKAO_BOOK_SEARCH_URL

@rt.get('/')
async def search_books(name: str):
    params = {"query": name}
    headers = {'Authorization': "KakaoAK {}".format(Config.KAKAO_BOOK_SEARCH_API_KEY)}
    book_res = requests.get(url=URL, params=params, headers=headers)
    return book_res.json()

@rt.post('/')
async def create_book(book: BookInfo, db: Session = Depends(get_db)):
    existedBook = db.query(Book).filter(Book.author)
    pass