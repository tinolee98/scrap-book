from typing import List
from pydantic import BaseModel, Field

from src.routes.apis.v1.book.schemas import BookIn

class ResScrapbook(BaseModel):
    id: int = Field(..., title='스크랩북 id', example='1')
    bookId: int = Field(..., title='책 id', example='1')
    uuid: str = Field(..., title='스크랩북 uuid', example='12341234')
    createdAt: str = Field(..., title='생성 날짜', example='2022-01-01T00:00:00')
    updatedAt: str = Field(..., title='수정 날짜', example='2022-01-01T00:00:00')
    star: bool = Field(..., title='즐겨찾기 유무', example=True)
    book: BookIn = Field(..., title='스크랩북의 책 정보')

class ResScrapbooks(BaseModel):
    scrapbooks: List[ResScrapbook] = Field(...)