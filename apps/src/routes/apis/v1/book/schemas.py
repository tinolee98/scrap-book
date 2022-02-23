from pydantic import BaseModel

class BookIn(BaseModel):
    title: str
    authors: str
    publisher: str
    contents: str
    thumbnail: str
    url: str

