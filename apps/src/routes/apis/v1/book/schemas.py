from pydantic import BaseModel, Field

class BookIn(BaseModel):
    title: str = Field(..., title='책 제목', example='논어')
    authors: str = Field(..., title='책 저자', example='공자')
    publisher: str = Field(..., title='출판사', example='책 출판사')
    contents: str = Field(..., title='책 줄거리', example='논어는 말입니다...')
    thumbnail: str = Field(..., title='책 표지', example='http://thumbnail.com')
    url: str = Field(..., title='책 설명 주소', example='http://url.com')

