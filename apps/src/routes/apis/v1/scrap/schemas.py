from typing import List, Optional, Text
from pydantic import BaseModel, Field

from src.common.schema import OkError

class ResScrap(BaseModel):
    text: Text = Field(..., title='스크랩 설명', example='스크랩에 대한 나의 의견을 적는 공간입니다.')
    page: int = Field(..., title='스크랩 책 페이지', example='123')
    picture_url: str = Field(..., title='스크랩 이미지 url', example='http://pictureUrl.com')
    class config:
        orm_mode = True

class ResScraps(BaseModel):
    scraps: List[ResScrap]
    class config:
        orm_mode = True