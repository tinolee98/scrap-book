from pydantic import BaseModel

class BookInfo(BaseModel):
    title: str
    author: str
    publisher: str
    contents: str
    thumbnail: str
    detailUrl: str

