import requests
import json
import httpx
import asyncio
from time import time

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import Field
from sqlalchemy.orm import Session

from src.sql.database import get_db
from src.service.user import UserService
from src.config import Config

rt = APIRouter(prefix='/apis/v1/book', tags=['/apis/v1/book'])
URL = Config.KAKAO_BOOK_SEARCH_URL

async def request(client):
    res = await client.get(URL)
    return res.text

async def task():
    async with httpx.AsyncClient() as client:
        tasks = [request(client) for i in range(10)]
        result = await asyncio.gather(*tasks)
        print(result)

@rt.get('/')
async def search_books(name: str):
    params = {"query": name}
    headers = {'Authorization': "KakaoAK {}".format(Config.KAKAO_BOOK_SEARCH_API_KEY)}
    book_res = requests.get(url=URL, params=params, headers=headers)
    return book_res.json()
